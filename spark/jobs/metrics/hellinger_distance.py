import itertools
import math
from typing import Optional

import numpy as np
from pyspark.sql import DataFrame, functions as f
from scipy.stats import gaussian_kde
from utils.drift_detector import DriftDetector
from utils.models import ColumnDefinition, DriftAlgorithmType, FieldTypes


class HellingerDistance(DriftDetector):
    """Class for performing the Hellinger Distance using Pyspark."""

    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs['threshold']:
            raise AttributeError('threshold is not defined in kwargs')
        threshold = kwargs['threshold']
        feature_dict_to_append['type'] = DriftAlgorithmType.HELLINGER
        feature_dict_to_append['limit'] = threshold
        result_tmp = self.compute_distance(feature.name, feature.field_type)
        if result_tmp['HellingerDistance'] is None or math.isnan(
            result_tmp['HellingerDistance']
        ):
            feature_dict_to_append['value'] = -1
            feature_dict_to_append['has_drift'] = False
            return feature_dict_to_append
        feature_dict_to_append['value'] = float(result_tmp['HellingerDistance'])
        feature_dict_to_append['has_drift'] = bool(
            result_tmp['HellingerDistance'] > threshold
        )
        return feature_dict_to_append

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.categorical, FieldTypes.numerical]

    def __init__(self, spark_session, reference_data, current_data, prefix_id) -> None:
        """Initialize the Hellinger Distance object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data
        - reference_data_length (int): The reference length
        - current_data_length (int): The current length

        """
        self.spark_session = spark_session
        # Optimized: Cache after dropna to avoid re-scanning
        self.reference_data = reference_data.dropna().cache()
        self.current_data = current_data.dropna().cache()
        self.reference_data_length = self.reference_data.count()
        self.current_data_length = self.current_data.count()
        self.prefix_id = prefix_id

    @staticmethod
    def __calculate_category_percentages(
        df: DataFrame, column_name: str, prefix_id: str
    ) -> DataFrame:
        """Create a new dataframe with categories and their percentages

        Parameters:
        - df (pyspark.sql.DataFrame): The spark df
        - column_name (str): The name of the categorical column

        Returns:
        DataFrame with two columns: category and percentage

        """
        category_counts = df.groupBy(column_name).agg(
            f.count('*').alias(f'{prefix_id}_count')
        )
        # Optimized: Calculate total from aggregated results instead of full scan
        total_count = category_counts.agg(f.sum(f'{prefix_id}_count')).first()[0]
        result_df = category_counts.withColumn(
            f'{prefix_id}_percentage',
            (f.col(f'{prefix_id}_count') / f.lit(total_count)),
        )
        return result_df.select(
            f.col(column_name).alias(f'{prefix_id}_category'),
            f.col(f'{prefix_id}_percentage'),
        ).orderBy(f'{prefix_id}_category')

    @staticmethod
    def __calculate_kde_continuous_pdf_on_partition(
        df: DataFrame, column_name: str, bins: int
    ) -> list:
        """Estimate the probability density function using KDE for each partition (workers).

        Parameters:
        - df (pyspark.sql.DataFrame): The spark df
        - column_name (str): The name of the continuous column
        - bins (int): The number of bins

        Returns:
        A list with the KDE processing for each worker.

        """

        def __compute_kde_on_partition(iterator):
            array_on_parts = np.array(list(iterator)).reshape(-1)
            kde = gaussian_kde(array_on_parts)
            x = np.linspace(min(array_on_parts), max(array_on_parts), bins)
            pdf = kde.evaluate(x)
            yield x, pdf / np.sum(pdf), len(array_on_parts)

        rdd_data = df.select(column_name).rdd
        return rdd_data.mapPartitions(__compute_kde_on_partition).collect()

    @staticmethod
    def __calculate_kde_continuous_pdf(
        df: DataFrame, column_name: str, bins: int
    ) -> tuple:
        """Estimate the probability density function using KDE.

        Parameters:
        - df (pyspark.sql.DataFrame): The spark df
        - column_name (str): The name of the continuous column
        - bins (int): The number of bins

        Returns:
        Tuple with two objects: the interpolation points and the pdf

        """
        np_array = np.array(df.select(column_name).rdd.flatMap(lambda xi: xi).collect())
        kde = gaussian_kde(np_array)
        x = np.linspace(min(np_array), max(np_array), bins)
        pdf = kde.evaluate(x)
        return x, pdf / np.sum(pdf)

    def __compute_bins_for_continuous_data(self) -> int:
        """Calculate the number of bins using the Sturges rule.

        Returns:
        Bins number as integer.

        """
        return int(np.ceil(np.log2(self.reference_data_length) + 1))

    def __hellinger_distance(
        self,
        column_name: str,
        data_type: FieldTypes,
        process_on_partitions: bool = False,
    ) -> Optional[float]:
        """Compute the Hellinger Distasnce according to the data type (discrete or continuous).

        Parameters:
        - column_name (str): The name of the column
        - data_type (str): The type of the field (discrete or continuous)
        - process_on_partitions (bool): If it is True, partition processing is activated (False by default)

        Returns:
        The Hellinger Distance value.

        """
        column = column_name

        if data_type == FieldTypes.categorical:
            reference_category_percentages = self.__calculate_category_percentages(
                df=self.reference_data, column_name=column, prefix_id=self.prefix_id
            )

            current_category_percentages = self.__calculate_category_percentages(
                df=self.current_data, column_name=column, prefix_id=self.prefix_id
            )

            # Optimized: Use collect() instead of toPandas() for better performance
            reference_rows = reference_category_percentages.collect()
            current_rows = current_category_percentages.collect()

            reference_category_dict = {
                row[f'{self.prefix_id}_category']: row[f'{self.prefix_id}_percentage']
                for row in reference_rows
            }

            current_category_dict = {
                row[f'{self.prefix_id}_category']: row[f'{self.prefix_id}_percentage']
                for row in current_rows
            }

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
            if reference_category_dict.keys() != current_category_dict.keys():
                dicts = (reference_category_dict, current_category_dict)
                all_keys = set().union(*dicts)
                reference_category_dict, current_category_dict = (
                    {key: d.get(key, 0.0) for key in all_keys} for d in dicts
                )

            reference_values = np.array(list(reference_category_dict.values()))
            current_values = np.array(list(current_category_dict.values()))

            return np.sqrt(
                0.5 * np.sum((np.sqrt(reference_values) - np.sqrt(current_values)) ** 2)
            )

        if data_type == FieldTypes.numerical:
            bins = self.__compute_bins_for_continuous_data()

            if process_on_partitions:
                reference_pdf_part = self.__calculate_kde_continuous_pdf_on_partition(
                    df=self.reference_data, column_name=column, bins=bins
                )

                current_pdf_part = self.__calculate_kde_continuous_pdf_on_partition(
                    df=self.current_data, column_name=column, bins=bins
                )

                flat_x1_ref = list(
                    itertools.chain(*[list(i[0]) for i in reference_pdf_part])
                )
                ref_x1_min = min(flat_x1_ref)
                ref_x1_max = max(flat_x1_ref)

                flat_x2_cur = list(
                    itertools.chain(*[list(i[0]) for i in current_pdf_part])
                )
                cur_x2_min = min(flat_x2_cur)
                cur_x2_max = max(flat_x2_cur)

                # Find grid for both ref and current
                common_x_part = np.linspace(
                    min(ref_x1_min.min(), cur_x2_min.min()),
                    max(ref_x1_max.max(), cur_x2_max.max()),
                    bins,
                )

                # Compute weights based on sample size (data in the partition)
                ref_weights = [
                    i[2] / self.reference_data_length for i in reference_pdf_part
                ]
                cur_weights = [
                    i[2] / self.current_data_length for i in current_pdf_part
                ]

                # Overall KDE
                ref_overall_kde_pdf = sum(
                    [
                        w * x
                        for w, x in zip(ref_weights, [i[1] for i in reference_pdf_part])
                    ]
                )
                cur_overall_kde_pdf = sum(
                    [
                        w * x
                        for w, x in zip(cur_weights, [i[1] for i in current_pdf_part])
                    ]
                )

                percentile_values_for_x = np.linspace(0, 100, bins)

                reference_values_part = np.interp(
                    common_x_part,
                    np.percentile(flat_x1_ref, percentile_values_for_x),
                    ref_overall_kde_pdf,
                )

                current_values_part = np.interp(
                    common_x_part,
                    np.percentile(flat_x2_cur, percentile_values_for_x),
                    cur_overall_kde_pdf,
                )

                return np.sqrt(
                    0.5
                    * np.sum(
                        (np.sqrt(reference_values_part) - np.sqrt(current_values_part))
                        ** 2
                    )
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
        return None

    def compute_distance(self, on_column: str, data_type: FieldTypes) -> dict:
        """Return the Hellinger Distance.

        Parameters:
        - on_column (str): The column to use for the distance computation
        - data_type (str): The type of the field (discrete or continuous)

        Returns:
        The distance as a dictionary.

        """

        return {
            'HellingerDistance': self.__hellinger_distance(
                # We set process_on_partition=False until we find a strategy to
                # automatically select the proper processing type.
                column_name=on_column,
                data_type=data_type,
                process_on_partitions=False,
            )
        }
