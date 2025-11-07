import math
from typing import Dict

import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.stat import ChiSquareTest
import pyspark.sql
from pyspark.sql import DataFrame, SparkSession
import pyspark.sql.functions as F
from scipy.stats import chisquare
from utils.drift_detector import DriftDetector
from utils.models import ColumnDefinition, DriftAlgorithmType, FieldTypes


class Chi2Test(DriftDetector):
    """Class for performing a chi-square test of independence using Pyspark."""

    def __init__(
        self,
        spark_session: SparkSession,
        reference_data: DataFrame,
        current_data: DataFrame,
        prefix_id: str,
    ) -> None:
        """Initialize the Chi2Test object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object.
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data.
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data.
        - prefix_id (str): Prefix.

        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.prefix_id = prefix_id

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.categorical]

    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs['p_value']:
            raise AttributeError('p_value is not defined in kwargs')
        p_value = kwargs['p_value']
        feature_dict_to_append['type'] = DriftAlgorithmType.CHI2
        feature_dict_to_append['limit'] = p_value
        result_tmp = self.test_goodness_fit(feature.name, feature.name)
        if result_tmp['pValue'] is None or math.isnan(result_tmp['pValue']):
            feature_dict_to_append['value'] = -1
            feature_dict_to_append['has_drift'] = False
            return feature_dict_to_append
        feature_dict_to_append['value'] = float(result_tmp['pValue'])
        feature_dict_to_append['has_drift'] = bool(result_tmp['pValue'] <= p_value)
        return feature_dict_to_append

    def __have_same_size(self) -> bool:
        """Check if the reference and current data have the same size.

        Returns:
        - bool: True if the sizes are equal, False otherwise.

        """
        return bool(self.reference_size == self.current_size)

    def __concatenate_columns(self) -> pyspark.sql.DataFrame:
        """Concatenates the reference and current data if they have the same size or creates subsamples to make them
         of equal size.

        Returns:
        - pyspark.sql.DataFrame: The concatenated DataFrame.

        """
        if self.__have_same_size():
            # Optimized: Use DataFrame API instead of RDD conversions
            self.reference = self.reference.withColumn(
                'id', F.monotonically_increasing_id()
            )
            self.current = self.current.withColumn(
                'id', F.monotonically_increasing_id()
            )
            concatenated_data = self.reference.join(
                self.current, self.reference.id == self.current.id, how='inner'
            )

        else:
            max_size = max(self.reference_size, self.current_size)

            if self.reference_size == max_size:
                # Optimized: Use distributed sample instead of takeSample
                fraction = self.current_size / self.reference_size
                subsample_reference = (
                    self.reference.sample(
                        withReplacement=True, fraction=fraction, seed=1990
                    )
                    .limit(self.current_size)
                    .withColumn('id', F.monotonically_increasing_id())
                )
                self.current = self.current.withColumn(
                    'id', F.monotonically_increasing_id()
                )
                concatenated_data = subsample_reference.join(
                    self.current, subsample_reference.id == self.current.id, how='inner'
                )
            else:
                # Optimized: Use distributed sample instead of takeSample
                fraction = self.reference_size / self.current_size
                subsample_current = (
                    self.current.sample(
                        withReplacement=True, fraction=fraction, seed=1990
                    )
                    .limit(self.reference_size)
                    .withColumn('id', F.monotonically_increasing_id())
                )
                self.reference = self.reference.withColumn(
                    'id', F.monotonically_increasing_id()
                )
                concatenated_data = subsample_current.join(
                    self.reference,
                    subsample_current.id == self.reference.id,
                    how='inner',
                )

        return concatenated_data

    @staticmethod
    def __numeric_casting(
        concatenated_data: DataFrame, reference_column: str, current_column: str
    ) -> pyspark.sql.DataFrame:
        """Perform numeric casting on the concatenated data.

        Parameters:
        - concatenated_data (pyspark.sql.DataFrame): The concatenated DataFrame.
        - reference_column (str): reference_column
        - current_column (str): current_column

        Returns:
        - pyspark.sql.DataFrame: The DataFrame with numeric casting applied.

        """
        # Optimized: Single pipeline fit instead of double fitting
        indexers = [
            StringIndexer(inputCol=column, outputCol=f'{column}_index')
            for column in [reference_column, current_column]
        ]
        pipeline = Pipeline(stages=indexers)
        fitted_pipeline = pipeline.fit(concatenated_data)
        return (
            fitted_pipeline.transform(concatenated_data)
            .drop(reference_column, current_column)
            .withColumnRenamed(f'{reference_column}_index', reference_column)
            .withColumnRenamed(f'{current_column}_index', current_column)
        )

    @staticmethod
    def __current_column_to_vector(
        data: DataFrame, reference_column: str, current_column: str
    ) -> pyspark.sql.DataFrame:
        """Convert the current column data to a vector using VectorAssembler.

        Parameters:
        - data (pyspark.sql.DataFrame): The DataFrame containing the data.
        - reference_column (str): reference_column
        - current_column (str): current_column

        Returns:
        - pyspark.sql.DataFrame: The DataFrame with the current column data converted to a vector.

        """
        vector_assembler = VectorAssembler(
            inputCols=[current_column],
            outputCol=f'{current_column}_vector',
            handleInvalid='skip',
        )
        return vector_assembler.transform(data).select(
            reference_column, f'{current_column}_vector'
        )

    def __prepare_data_for_test(
        self, reference_column: str, current_column: str
    ) -> pyspark.sql.DataFrame:
        """Prepare the data for the chi-square test by concatenating columns, performing numeric casting, and converting
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
        return self.__current_column_to_vector(
            data=numeric_concatenated_data,
            reference_column=reference_column,
            current_column=current_column,
        )

    def test_independence(self, reference_column: str, current_column: str) -> Dict:
        """Performs the chi-square test of independence.

        Parameters:
        - reference_column (str): The column name in the reference DataFrame to test
        - current_column (str): The column name in the current DataFrame to test

        Returns:
        - dict: A dictionary containing the test results including p-value, degrees of freedom, and statistic.

        """
        # Optimized: Filter pushdown - apply na.drop early
        self.reference = (
            self.reference_data.na.drop(subset=[reference_column])
            .select(reference_column)
            .withColumnRenamed(reference_column, f'{reference_column}_reference')
        )
        self.current = (
            self.current_data.na.drop(subset=[current_column])
            .select(current_column)
            .withColumnRenamed(current_column, f'{current_column}_current')
        )
        reference_column = f'{reference_column}_reference'
        current_column = f'{current_column}_current'

        # Optimized: Cache before count to avoid re-scanning
        self.reference = self.reference.cache()
        self.current = self.current.cache()
        self.reference_size = self.reference.count()
        self.current_size = self.current.count()

        result = ChiSquareTest.test(
            self.__prepare_data_for_test(reference_column, current_column),
            f'{current_column}_vector',
            reference_column,
            True,
        )

        # Optimized: Single collect() call instead of three
        row = result.select('pValue', 'degreesOfFreedom', 'statistic').first()

        # Clean up cache
        self.reference.unpersist()
        self.current.unpersist()

        return {
            'pValue': row['pValue'],
            'degreesOfFreedom': row['degreesOfFreedom'],
            'statistic': row['statistic'],
        }

    def test_goodness_fit(self, reference_column, current_column) -> dict:
        """Performs the chi-square goodness of fit test.

        Returns:
        - dict: A dictionary containing the test results including p-value and statistic.

        """
        # Optimized: Filter pushdown - apply na.drop early
        self.reference = (
            self.reference_data.na.drop(subset=[reference_column])
            .select(reference_column)
            .withColumnRenamed(reference_column, f'{self.prefix_id}_value')
        )
        self.current = (
            self.current_data.na.drop(subset=[current_column])
            .select(current_column)
            .withColumnRenamed(current_column, f'{self.prefix_id}_value')
        )

        # Optimized: Cache before count to avoid re-scanning
        self.reference = self.reference.cache()
        self.current = self.current.cache()
        self.reference_size = self.reference.count()
        self.current_size = self.current.count()

        self.current = self.current.withColumn('type', F.lit('current'))
        self.reference = self.reference.withColumn('type', F.lit('reference'))

        # Optimized: Cache concatenated_data as it's used twice
        concatenated_data = self.current.unionByName(self.reference).cache()

        def cnt_cond(cond):
            return F.sum(F.when(cond, 1).otherwise(0))

        # Optimized: Single groupBy with both aggregations instead of two separate groupBy operations
        counts = (
            concatenated_data.groupBy(f'{self.prefix_id}_value')
            .agg(
                cnt_cond(F.col('type') == 'reference').alias('ref_count'),
                cnt_cond(F.col('type') == 'current').alias('cur_count'),
            )
            .collect()
        )

        # Extract arrays from single collect result
        ref_fr = np.array([row['ref_count'] for row in counts])
        cur_fr = np.array([row['cur_count'] for row in counts])

        # Clean up caches
        concatenated_data.unpersist()
        self.reference.unpersist()
        self.current.unpersist()

        proportion = sum(cur_fr) / sum(ref_fr)
        ref_fr = ref_fr * proportion
        res = chisquare(cur_fr, ref_fr)
        return {'pValue': float(res[1]), 'statistic': float(res[0])}
