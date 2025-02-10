from typing import Dict
import numpy as np
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from scipy.stats import wasserstein_distance


class WassersteinDistance:
    """Class for performing the Wasserstein Distance using Pyspark."""

    def __init__(self, spark_session, reference_data, current_data) -> None:
        """
        Initializes the Wasserstein Distance object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data
        - reference_data_length (int): The reference length
        - current_data_length (int): The current length
        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.reference_data_length = self.reference_data.count()
        self.current_data_length = self.current_data.count()

    @staticmethod
    def __wasserstein_distance(
        df_reference: DataFrame, df_current: DataFrame, column_name: str
    ) -> float:
        """
        Estimate the distance from reference and current values.

        Parameters:
        - df (pyspark.sql.DataFrame): The spark df
        - column_name (str): The name of the continuous column
        - bins (int): The number of bins

        Returns:
        Tuple with two objects: the interpolation points and the pdf
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

    def return_distance(self, on_column: str) -> Dict:
        """
        Returns the Wasserstein Distance.

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
