from typing import Dict, List
import pyspark.sql
from pyspark.ml.stat import ChiSquareTest
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml import Pipeline
import pyspark.sql.functions as F
import numpy as np
from pyspark.sql import SparkSession, DataFrame
from scipy.stats import chisquare

from metrics.drift_factory_pattern import DriftDetector, DriftDetectionResult, DriftAlgorithmType
from utils.models import FieldTypes


class Chi2Test(DriftDetector):
    """Class for performing a chi-square test of independence using Pyspark."""

    def __init__(self, spark_session: SparkSession, reference_data: DataFrame, current_data: DataFrame, prefix_id: str) -> None:
        """
        Initializes the Chi2Test object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object.
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data.
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data.
        - reference_column (str): The column name in the reference data DataFrame.
        - current_column (str): The column name in the current data DataFrame.
        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.prefix_id = prefix_id

    @property
    def supported_feature_types(self) -> List[FieldTypes]:
        return [FieldTypes.categorical]

    def detect_drift(self, feature: str) -> DriftDetectionResult:
        feature_dict_to_append = {
            "feature_name": feature,
            "field_type": FieldTypes.categorical.value,
            "drift_calc": {
                "type": DriftAlgorithmType.CHI2,
            },
        }
        result_tmp = self.test_goodness_fit(feature, feature)
        feature_dict_to_append["drift_calc"]["value"] = float(result_tmp["pValue"])
        feature_dict_to_append["drift_calc"]["has_drift"] = bool(
            result_tmp["pValue"] <= 0.05
        )
        return DriftDetectionResult.model_validate(feature_dict_to_append)

    def __have_same_size(self) -> bool:
        """
        Checks if the reference and current data have the same size.

        Returns:
        - bool: True if the sizes are equal, False otherwise.
        """
        return True if self.reference_size == self.current_size else False

    def __concatenate_columns(self) -> pyspark.sql.DataFrame:
        """
        Concatenates the reference and current data if they have the same size or creates subsamples to make them
         of equal size.

        Returns:
        - pyspark.sql.DataFrame: The concatenated DataFrame.
        """

        if self.__have_same_size():
            self.reference = (
                self.reference.rdd.flatMap(lambda x: x)
                .zipWithIndex()
                .toDF(tuple(self.reference.columns + ["id"]))
            )
            self.current = (
                self.current.rdd.flatMap(lambda x: x)
                .zipWithIndex()
                .toDF(tuple(self.current.columns + ["id"]))
            )
            concatenated_data = self.reference.join(
                self.current, self.reference.id == self.current.id, how="inner"
            )

        else:
            max_size = max(self.reference_size, self.current_size)

            if self.reference_size == max_size:
                # create a reference subsample with a size equal to the current
                subsample_reference = (
                    self.spark_session.createDataFrame(
                        self.reference.rdd.takeSample(
                            withReplacement=True, num=self.current_size, seed=1990
                        )
                    )
                    .rdd.flatMap(lambda x: x)
                    .zipWithIndex()
                    .toDF(tuple(self.reference.columns + ["id"]))
                )
                self.current = (
                    self.current.rdd.flatMap(lambda x: x)
                    .zipWithIndex()
                    .toDF(tuple(self.current.columns + ["id"]))
                )
                concatenated_data = subsample_reference.join(
                    self.current, subsample_reference.id == self.current.id, how="inner"
                )
            else:
                # create a current subsample with a size equal to the reference
                subsample_current = (
                    self.spark_session.createDataFrame(
                        self.current.rdd.takeSample(
                            withReplacement=True, num=self.reference_size, seed=1990
                        )
                    )
                    .rdd.flatMap(lambda x: x)
                    .zipWithIndex()
                    .toDF(tuple(self.current.columns + ["id"]))
                )
                self.reference = (
                    self.reference.rdd.flatMap(lambda x: x)
                    .zipWithIndex()
                    .toDF(tuple(self.reference.columns + ["id"]))
                )
                concatenated_data = subsample_current.join(
                    self.reference,
                    subsample_current.id == self.reference.id,
                    how="inner",
                )

        return concatenated_data

    def __numeric_casting(
        self, concatenated_data, reference_column, current_column
    ) -> pyspark.sql.DataFrame:
        """
        Performs numeric casting on the concatenated data.

        Parameters:
        - concatenated_data (pyspark.sql.DataFrame): The concatenated DataFrame.

        Returns:
        - pyspark.sql.DataFrame: The DataFrame with numeric casting applied.
        """
        indexers = [
            StringIndexer(inputCol=column, outputCol=column + "_index").fit(
                concatenated_data
            )
            for column in [reference_column, current_column]
        ]
        pipeline = Pipeline(stages=indexers)
        return (
            pipeline.fit(concatenated_data)
            .transform(concatenated_data)
            .drop(reference_column, current_column)
            .withColumnRenamed(reference_column + "_index", reference_column)
            .withColumnRenamed(current_column + "_index", current_column)
        )

    def __current_column_to_vector(
        self, data, reference_column, current_column
    ) -> pyspark.sql.DataFrame:
        """
        Converts the current column data to a vector using VectorAssembler.

        Parameters:
        - data (pyspark.sql.DataFrame): The DataFrame containing the data.

        Returns:
        - pyspark.sql.DataFrame: The DataFrame with the current column data converted to a vector.
        """
        vector_assembler = VectorAssembler(
            inputCols=[current_column],
            outputCol=f"{current_column}_vector",
            handleInvalid="skip",
        )
        return vector_assembler.transform(data).select(
            reference_column, f"{current_column}_vector"
        )

    def __prepare_data_for_test(
        self, reference_column, current_column
    ) -> pyspark.sql.DataFrame:
        """
        Prepares the data for the chi-square test by concatenating columns, performing numeric casting, and converting
        the current column data to a vector.

        Returns:
        - pyspark.sql.DataFrame: The prepared DataFrame for the chi-square test.
        """
        concatenated_data = self.__concatenate_columns()
        numeric_concatenated_data = self.__numeric_casting(
            concatenated_data=concatenated_data,
            reference_column=reference_column,
            current_column=current_column,
        )
        vector_data = self.__current_column_to_vector(
            data=numeric_concatenated_data,
            reference_column=reference_column,
            current_column=current_column,
        )
        return vector_data.select(reference_column, f"{current_column}_vector")

    def test_independence(self, reference_column, current_column) -> Dict:
        """
        Performs the chi-square test of independence.

        Parameters:
        - reference_column (string): The column name in the reference DataFrame to test
        - current_column (string): The column name in the current DataFrame to test

        Returns:
        - dict: A dictionary containing the test results including p-value, degrees of freedom, and statistic.
        """
        self.reference = (
            self.reference_data.select(reference_column)
            .withColumnRenamed(reference_column, f"{reference_column}_reference")
            .drop(*[reference_column])
            .na.drop()
        )
        self.current = (
            self.current_data.select(current_column)
            .withColumnRenamed(current_column, f"{current_column}_current")
            .drop(*[current_column])
            .na.drop()
        )
        reference_column = f"{reference_column}_reference"
        current_column = f"{current_column}_current"
        self.reference_size = self.reference.count()
        self.current_size = self.current.count()
        result = ChiSquareTest.test(
            self.__prepare_data_for_test(reference_column, current_column),
            f"{current_column}_vector",
            reference_column,
            True,
        )

        return {
            "pValue": result.select("pValue").collect()[0][0],
            "degreesOfFreedom": result.select("degreesOfFreedom").collect()[0][0],
            "statistic": result.select("statistic").collect()[0][0],
        }

    def test_goodness_fit(self, reference_column, current_column) -> Dict:
        """
        Performs the chi-square goodness of fit test.

        Returns:
        - dict: A dictionary containing the test results including p-value and statistic.
        """

        self.reference = (
            self.reference_data.select(reference_column)
            .withColumnRenamed(reference_column, f"{self.prefix_id}_value")
            .na.drop()
        )
        self.current = (
            self.current_data.select(current_column)
            .withColumnRenamed(current_column, f"{self.prefix_id}_value")
            .na.drop()
        )
        self.reference_size = self.reference.count()
        self.current_size = self.current.count()

        self.current = self.current.withColumn("type", F.lit("current"))
        self.reference = self.reference.withColumn("type", F.lit("reference"))

        concatenated_data = self.current.unionByName(self.reference)

        def cnt_cond(cond):
            return F.sum(F.when(cond, 1).otherwise(0))

        ref_fr = np.array(
            concatenated_data.groupBy(f"{self.prefix_id}_value")
            .agg(
                cnt_cond(F.col("type") == "reference").alias(f"{self.prefix_id}_count")
            )
            .select(f"{self.prefix_id}_count")
            .rdd.flatMap(lambda x: x)
            .collect()
        )
        cur_fr = np.array(
            concatenated_data.groupBy(f"{self.prefix_id}_value")
            .agg(cnt_cond(F.col("type") == "current").alias(f"{self.prefix_id}_count"))
            .select(f"{self.prefix_id}_count")
            .rdd.flatMap(lambda x: x)
            .collect()
        )
        proportion = sum(cur_fr) / sum(ref_fr)
        ref_fr = ref_fr * proportion
        res = chisquare(cur_fr, ref_fr)
        return {"pValue": float(res[1]), "statistic": float(res[0])}
