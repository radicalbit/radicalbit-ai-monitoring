from typing import Dict
import numpy as np
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from scipy.stats import wasserstein_distance

from utils.drift_detector import DriftDetector
from utils.models import FieldTypes, ColumnDefinition, DriftAlgorithmType


class WassersteinDistance(DriftDetector):
    """Class for performing the Wasserstein Distance using Pyspark."""

    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs["threshold"]:
            raise AttributeError(f"threshold is not defined in kwargs")
        threshold = kwargs["threshold"]
        result_tmp = self.compute_distance(feature.name)
        feature_dict_to_append["type"] = DriftAlgorithmType.WASSERSTEIN
        feature_dict_to_append["value"] = float(result_tmp["WassersteinDistance"])
        feature_dict_to_append["has_drift"] = bool(
            result_tmp["WassersteinDistance"] <= threshold
        )
        return feature_dict_to_append

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.numerical]

    def __init__(self, spark_session, reference_data, current_data, prefix_id) -> None:
        """
        Initializes the Wasserstein Distance object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data
        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.prefix_id = prefix_id

    @staticmethod
    def __wasserstein_distance(
        df_reference: DataFrame, df_current: DataFrame, column_name: str
    ) -> float:
        """
        Estimate the distance from reference and current values.

        Parameters:
        - df_reference (pyspark.sql.DataFrame): The reference dataset
        - df_current (pyspark.sql.DataFrame): The current dataset
        - column_name (str): The name of the continuous column


        Returns:
        Float with computed distance
        """

        reference_values = np.array(
            df_reference.select(column_name)
            .filter(f.col(column_name).isNotNull())
            .rdd.flatMap(lambda xi: xi)
            .collect()
        )
        current_values = np.array(
            df_current.select(column_name)
            .filter(f.col(column_name).isNotNull())
            .rdd.flatMap(lambda xi: xi)
            .collect()
        )

        return wasserstein_distance(reference_values, current_values)

    def compute_distance(self, on_column: str) -> Dict:
        """
        Returns the Wasserstein Distance as a dictionary.

        Parameters:
        - on_column (str): The column to use for the distance computation
        - data_type (str): The type of the field (discrete or continuous)

        Returns:
        The distance as a dictionary.
        """

        return {
            "WassersteinDistance": self.__wasserstein_distance(
                df_reference=self.reference_data,
                df_current=self.current_data,
                column_name=on_column,
            )
        }
