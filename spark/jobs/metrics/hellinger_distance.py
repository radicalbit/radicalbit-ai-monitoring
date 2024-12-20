from typing import Tuple, Optional, Dict
import numpy as np
from pyspark.sql import functions as F
from pyspark.sql import DataFrame
from scipy.stats import gaussian_kde


class HellingerDistance:
    """Class for performing the Hellinger Distance using Pyspark."""

    def __init__(self, spark_session, reference_data, current_data) -> None:
        """
        Initializes the Hellinger Distance object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object.
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data.
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data.
        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data

    @staticmethod
    def __calculate_category_percentages(df: DataFrame, column_name: str) -> DataFrame:
        """
        Creates a new dataframe with categories and their percentages

        Parameters:
        df: spark DataFrame
        column_name: str, name of the categorical column

        Returns:
        DataFrame with two columns: category and percentage
        """

        category_counts = df.groupBy(column_name).agg(F.count("*").alias("count"))
        total_count = df.count()
        result_df = category_counts.withColumn(
            "percentage", (F.col("count") / F.lit(total_count))
        )
        return result_df.select(
            F.col(column_name).alias("category"), F.col("percentage")
        ).orderBy("category")

    @staticmethod
    def __calculate_kde_continuous_pdf(
        df: DataFrame, column_name: str, bins: int
    ) -> Tuple:
        """
        Estimate the probability density function using KDE.

        Parameters:
        df: spark DataFrame
        column_name: str, name of the categorical column
        bins: the number of bins to use

        Returns:
        Tuple with two objects: the interpolation points and the pdf
        """

        np_array = np.array(df.select(column_name).rdd.flatMap(lambda xi: xi).collect())
        kde = gaussian_kde(np_array)
        x = np.linspace(min(np_array), max(np_array), bins)
        pdf = kde.evaluate(x)
        return x, pdf / np.sum(pdf)

    def __compute_bins_for_continuous_data(
        self, column: str, method: str = "sturges"
    ) -> int:
        """
        Calculate the number of bins using the Sturges rule (default) or the Freedman-Diaconis Rule.

        Parameters:
        column: it is the column to use for binning computation
        method: it is the method to use for the binning. By default, Sturges rule is applied.

        Return:
        Bins number, int
        """

        n = self.reference_data.count()

        if method == "sturges":
            return int(np.ceil(np.log2(n) + 1))

        elif method == "freedman":
            # Calculate the 25th and 75th percentiles
            calculated_percentile = self.reference_data.select(
                F.percentile(column, 0.25), F.percentile(column, 0.75)
            ).collect()[0]

            q1, q3 = calculated_percentile[0], calculated_percentile[1]
            print(q1, q3)
            iqr = q3 - q1
            bin_width = (2 * iqr) / (n ** (1 / 3))

            # Find the minimum and maximum values
            min_max = self.reference_data.agg(
                F.min(column).alias("min_value"), F.max(column).alias("max_value")
            ).collect()[0]

            min_value = int(min_max["min_value"])
            max_value = int(min_max["max_value"])

            data_range = max_value - min_value

            return int(np.ceil(data_range / bin_width))

    def __hellinger_distance(self, column_name: str, data_type: str) -> Optional[float]:
        """
        Compute the Hellinger Distasnce according to the data type (discrete or continuous).

        Parameters:
        column_name: str
        data_type: str

        Returns:
        The Hellinger Distance value or a None if the data_type is not valid.
        """
        column = column_name

        if data_type == "discrete":
            reference_category_percentages = self.__calculate_category_percentages(
                df=self.reference_data, column_name=column
            )

            current_category_percentages = self.__calculate_category_percentages(
                df=self.current_data, column_name=column
            )

            reference_category_dict = (
                reference_category_percentages.toPandas()
                .set_index("category")["percentage"]
                .to_dict()
            )

            current_category_dict = (
                current_category_percentages.toPandas()
                .set_index("category")["percentage"]
                .to_dict()
            )

            """
            Note: Only for discrete variables!
            Check if reference and current have the same keys.
            If not, missing keys will be added in the shorter dictionary with a percentage of 0.0.
            For example:
            
            ref_dict = {"A": 0.5, "B": 0.5}
            curr_dict = {"A": 0.5, "B": 0.25, "C": 0.25}
            
            The ref_dict will be modified as follows:
            ref_dict = {"A": 0.5, "B": 0.5, "C": 0.0}
            """
            if not reference_category_dict.keys() == current_category_dict.keys():
                dicts = (reference_category_dict, current_category_dict)
                all_keys = set().union(*dicts)
                reference_category_dict, current_category_dict = [
                    {key: d.get(key, 0.0) for key in all_keys} for d in dicts
                ]

            reference_values = np.array(list(reference_category_dict.values()))
            current_values = np.array(list(current_category_dict.values()))

            return np.sqrt(
                0.5 * np.sum((np.sqrt(reference_values) - np.sqrt(current_values)) ** 2)
            )

        elif data_type == "continuous":
            bins = self.__compute_bins_for_continuous_data(
                column=column, method="sturges"
            )

            x1, reference_pdf = self.__calculate_kde_continuous_pdf(
                df=self.reference_data, column_name=column, bins=bins
            )

            x2, current_pdf = self.__calculate_kde_continuous_pdf(
                df=self.current_data, column_name=column, bins=bins
            )

            common_x = np.linspace(
                min(x1.min(), x2.min()), max(x1.max(), x2.max()), bins
            )
            reference_values = np.interp(common_x, x1, reference_pdf)
            current_values = np.interp(common_x, x2, current_pdf)

            return np.sqrt(
                0.5 * np.sum((np.sqrt(reference_values) - np.sqrt(current_values)) ** 2)
            )

        else:
            return None

    def return_distance(self, on_column: str, data_type: str) -> Dict:
        """
        Returns the Hellinger Distance.

        Parameters:
        on_column: the column to use for the distance computation
        data_type: the type of the field (discrete or continuous)

        Returns:
        The distance, Dict.
        """
        if not None:
            return {
                "HellingerDistance": self.__hellinger_distance(
                    column_name=on_column, data_type=data_type
                )
            }
