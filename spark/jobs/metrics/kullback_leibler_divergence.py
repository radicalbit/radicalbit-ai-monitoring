from pyspark.sql import DataFrame
import numpy as np
from typing import Tuple, Dict, Optional
from pyspark.sql import functions as f
from pyspark.ml.feature import Bucketizer

from utils.drift_detector import DriftDetector
from utils.models import FieldTypes, ColumnDefinition, DriftAlgorithmType


class KullbackLeiblerDivergence(DriftDetector):
    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs["threshold"]:
            raise AttributeError("threshold is not defined in kwargs")
        threshold = kwargs["threshold"]
        result_tmp = self.compute_distance(feature.name, feature.field_type.value)
        feature_dict_to_append["type"] = DriftAlgorithmType.KL
        feature_dict_to_append["value"] = float(result_tmp["KullbackLeiblerDivergence"])
        feature_dict_to_append["has_drift"] = bool(
            result_tmp["KullbackLeiblerDivergence"] <= threshold
        )
        return feature_dict_to_append

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.numerical, FieldTypes.categorical]

    def __init__(self, spark_session, reference_data, current_data, prefix_id) -> None:
        """
        Initializes the KL-div object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data
        - prefix_id (str): A prefix to assign to temporary fields
        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.prefix_id = prefix_id
        self.percentiles = [
            i / 10 for i in range(1, 10)
        ]  # percentiles to bucketize continuous variables
        self.relative_error = 0.05  # the error to assign to approxQuantile

    def __calculate_category_percentages(
        self, df: DataFrame, column_name: str
    ) -> DataFrame:
        """
        Creates a new dataframe with categories and their percentages

        Parameters:
        - df (pyspark.sql.DataFrame): The spark df
        - column_name (str): The name of the categorical column

        Returns:
        DataFrame with two columns: category and percentage
        """

        df = df.filter(f.col(column_name).isNotNull())
        total_count = df.count()

        category_counts = df.groupBy(column_name).agg(
            f.count("*").alias(f"{self.prefix_id}_count")
        )

        result_df = category_counts.withColumn(
            f"{self.prefix_id}_percentage",
            (f.col(f"{self.prefix_id}_count") / f.lit(total_count)),
        )
        return result_df.select(
            f.col(column_name).alias(f"{self.prefix_id}_category"),
            f.col(f"{self.prefix_id}_percentage"),
        ).orderBy(f"{self.prefix_id}_category")

    def __bucketize_continuous_values(
        self, df_reference: DataFrame, df_current: DataFrame, column_name: str
    ) -> Tuple[DataFrame, DataFrame]:
        """
        This function creates buckets from the reference and uses the same to split current data.

        Parameters:
        - df_reference (DataFrame): The reference
        - df_current (DataFrame): The current
        - column_name (str): The column to bucketize

        Returns:
        - A Tuple of DataFrames containing reference and current percentages
        """
        reference = df_reference.select(column_name).filter(
            f.col(column_name).isNotNull()
        )
        current = df_current.select(column_name).filter(f.col(column_name).isNotNull())

        reference_count = reference.count()
        current_count = current.count()

        reference_quantiles = reference.approxQuantile(
            column_name, self.percentiles, self.relative_error
        )
        reference_buckets = [-float(np.inf)] + reference_quantiles + [float(np.inf)]

        bucketizer = Bucketizer(
            splits=reference_buckets,
            inputCol=column_name,
            outputCol=f"{self.prefix_id}_bucket",
        )

        reference_with_buckets = bucketizer.setHandleInvalid("keep").transform(
            reference
        )

        reference_bucket_counts = reference_with_buckets.groupBy(
            f"{self.prefix_id}_bucket"
        ).agg(f.count("*").alias(f"{self.prefix_id}_count"))

        reference_bucket_percentages = (
            reference_bucket_counts.withColumn(
                f"{self.prefix_id}_percentage",
                (f.col(f"{self.prefix_id}_count") / f.lit(reference_count)),
            )
            .select(
                f.col(f"{self.prefix_id}_bucket"),
                f.col(f"{self.prefix_id}_percentage"),
            )
            .orderBy(f"{self.prefix_id}_bucket")
        )

        current_with_buckets = bucketizer.setHandleInvalid("keep").transform(current)

        current_bucket_counts = current_with_buckets.groupBy(
            f"{self.prefix_id}_bucket"
        ).agg(f.count("*").alias(f"{self.prefix_id}_count"))

        current_bucket_percentages = (
            current_bucket_counts.withColumn(
                f"{self.prefix_id}_percentage",
                (f.col(f"{self.prefix_id}_count") / f.lit(current_count)),
            )
            .select(
                f.col(f"{self.prefix_id}_bucket"),
                f.col(f"{self.prefix_id}_percentage"),
            )
            .orderBy(f"{self.prefix_id}_bucket")
        )

        return reference_bucket_percentages, current_bucket_percentages

    def __kullback_leibler_divergence(
        self, column_name: str, data_type: str
    ) -> Optional[float]:
        """
        Compute the KL-div according to the data type (discrete or continuous).

        Parameters:
        - column_name (str): The name of the column
        - data_type (str): The type of the field (discrete or continuous)

        Returns:
        None if at least one class (categorical variable) or bucket (continuous variable) is 0.0 in the current dataset,
         otherwise it returns the KL-divergence
        """
        column = column_name

        def align_dicts(reference_dict, current_dict) -> tuple:
            """
            Check if reference and current have the same keys.
            When reference and current don't have the same keys,
            missing keys will be added in the shorter dictionary
            with a percentage of 0.0.
            For example:

            reference_dict = {"A": 0.5, "B": 0.5}
            current_dict = {"A": 0.5, "B": 0.25, "C": 0.25}

            The reference_dict will be modified as follows:
            reference_dict = {"A": 0.5, "B": 0.5, "C": 0.0}

            Parameters:
            - reference_dict (dict): The percentage of data in the reference buckets
            - current_dict (dict): The percentage of data in the current buckets

            Returns:
            A tuple containing the aligned dictionaries.
            """

            dicts = (reference_dict, current_dict)
            all_keys = set().union(*dicts)
            reference_dict, current_dict = [
                {key: d.get(key, 0.0) for key in all_keys} for d in dicts
            ]
            return reference_dict, current_dict

        if data_type == "discrete":
            reference_category_percentages = self.__calculate_category_percentages(
                df=self.reference_data, column_name=column
            )

            current_category_percentages = self.__calculate_category_percentages(
                df=self.current_data, column_name=column
            )

            reference_category_dict = (
                reference_category_percentages.toPandas()
                .set_index(f"{self.prefix_id}_category")[f"{self.prefix_id}_percentage"]
                .to_dict()
            )

            current_category_dict = (
                current_category_percentages.toPandas()
                .set_index(f"{self.prefix_id}_category")[f"{self.prefix_id}_percentage"]
                .to_dict()
            )

            if not reference_category_dict.keys() == current_category_dict.keys():
                reference_category_dict, current_category_dict = align_dicts(
                    reference_category_dict, current_category_dict
                )

            reference_values = np.array(list(reference_category_dict.values()))
            current_values = np.array(list(current_category_dict.values()))

            return (
                None
                if np.any(current_values == 0.0)
                else np.sum(
                    reference_values * np.log(reference_values / current_values)
                )
            )

        elif data_type == "continuous":
            reference_bucket_percentage, current_bucket_percentage = (
                self.__bucketize_continuous_values(
                    df_reference=self.reference_data,
                    df_current=self.current_data,
                    column_name=column,
                )
            )

            reference_bucket_dict = (
                reference_bucket_percentage.toPandas()
                .set_index(f"{self.prefix_id}_bucket")[f"{self.prefix_id}_percentage"]
                .to_dict()
            )

            current_bucket_dict = (
                current_bucket_percentage.toPandas()
                .set_index(f"{self.prefix_id}_bucket")[f"{self.prefix_id}_percentage"]
                .to_dict()
            )

            if not reference_bucket_dict.keys() == current_bucket_dict.keys():
                reference_bucket_dict, current_bucket_dict = align_dicts(
                    reference_bucket_dict, current_bucket_dict
                )

            reference_values = np.array(list(reference_bucket_dict.values()))
            current_values = np.array(list(current_bucket_dict.values()))

            return (
                None
                if np.any(current_values == 0.0)
                else np.sum(
                    reference_values * np.log(reference_values / current_values)
                )
            )

    def compute_distance(self, on_column: str, data_type: str) -> Dict:
        """
        Returns the Kullback-Leibler Divergence.

        Parameters:
        - on_column (str): The column to use for the distance computation
        - data_type (str): The type of the field (discrete or continuous)

        Returns:
        The divergence as a dictionary.
        """

        return {
            "KullbackLeiblerDivergence": self.__kullback_leibler_divergence(
                column_name=on_column, data_type=data_type
            )
        }
