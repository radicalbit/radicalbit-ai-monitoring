import logging
import math
from typing import Optional

import numpy as np
from pyspark.errors.exceptions.captured import IllegalArgumentException
from pyspark.ml.feature import Bucketizer
from pyspark.sql import DataFrame, functions as f
from scipy.spatial.distance import jensenshannon
from utils.drift_detector import DriftDetector
from utils.logger import logger_config
from utils.models import ColumnDefinition, DriftAlgorithmType, FieldTypes

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


class JensenShannonDistance(DriftDetector):
    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        feature_dict_to_append = {}
        if not kwargs['threshold']:
            raise AttributeError('threshold is not defined in kwargs')
        threshold = kwargs['threshold']
        feature_dict_to_append['type'] = DriftAlgorithmType.JS
        feature_dict_to_append['value'] = -1.0
        feature_dict_to_append['has_drift'] = False
        feature_dict_to_append['limit'] = threshold
        try:
            result_tmp = self.compute_distance(feature.name, feature.field_type)
            if result_tmp['JensenShannonDistance'] is None or math.isnan(
                result_tmp['JensenShannonDistance']
            ):
                return feature_dict_to_append
            feature_dict_to_append.update(
                {
                    'value': float(result_tmp['JensenShannonDistance']),
                    'has_drift': bool(result_tmp['JensenShannonDistance'] > threshold),
                }
            )
        except IllegalArgumentException as e:
            logger.error(e.desc)
            return feature_dict_to_append
        else:
            return feature_dict_to_append

    @property
    def supported_feature_types(self) -> list[FieldTypes]:
        return [FieldTypes.categorical, FieldTypes.numerical]

    def __init__(self, spark_session, reference_data, current_data, prefix_id) -> None:
        """Initialize the Jensen-Shannon Distance object with necessary data and parameters.

        Parameters:
        - spark_session (SparkSession): The SparkSession object
        - reference_data (pyspark.sql.DataFrame): The DataFrame containing the reference data
        - current_data (pyspark.sql.DataFrame): The DataFrame containing the current data
        - rbit_prefix (str): A prefix to assign to temporary fields

        """
        self.spark_session = spark_session
        self.reference_data = reference_data
        self.current_data = current_data
        self.prefix_id = prefix_id
        self.percentiles = [i / 10 for i in range(1, 10)]
        self.relative_error = 0.05

    def __calculate_category_percentages(
        self, df: DataFrame, column_name: str
    ) -> DataFrame:
        """Create a new dataframe with categories and their percentages

        Parameters:
        - df (pyspark.sql.DataFrame): The spark df
        - column_name (str): The name of the categorical column

        Returns:
        DataFrame with two columns: category and percentage

        """
        # OPTIMIZATION 1: Filter before select for better pushdown
        # OPTIMIZATION 2: Cache filtered data since used multiple times
        # OPTIMIZATION 3: Combine count with aggregation in single pass
        filtered_df = df.filter(f.col(column_name).isNotNull()).cache()

        # Single pass: groupBy with aggregation
        category_counts = filtered_df.groupBy(column_name).agg(
            f.count('*').alias(f'{self.prefix_id}_count')
        )

        # Calculate total from aggregated counts instead of separate count() action
        total_count_row = category_counts.agg(
            f.sum(f'{self.prefix_id}_count').alias('total')
        ).collect()[0]
        total_count = total_count_row['total']

        # Unpersist as no longer needed
        filtered_df.unpersist()

        result_df = category_counts.withColumn(
            f'{self.prefix_id}_percentage',
            (f.col(f'{self.prefix_id}_count') / f.lit(total_count)),
        )
        # OPTIMIZATION 4: Remove unnecessary orderBy (order not needed for JS distance)
        return result_df.select(
            f.col(column_name).alias(f'{self.prefix_id}_category'),
            f.col(f'{self.prefix_id}_percentage'),
        )

    def __bucketize_continuous_values(
        self, df_reference: DataFrame, df_current: DataFrame, column_name: str
    ) -> tuple[DataFrame, DataFrame]:
        """Create 10 buckets from the reference and uses the same to split current data.

        Parameters:
        - df_reference (DataFrame): The reference
        - df_current (DataFrame): The current
        - column_name (str): The column to bucketize

        Returns:
        - A Tuple of DataFrames containing reference and current percentages

        """
        # OPTIMIZATION 1: Filter before select for better pushdown
        # OPTIMIZATION 2: Cache filtered DataFrames since they're used multiple times
        reference = (
            df_reference.filter(f.col(column_name).isNotNull())
            .select(column_name)
            .cache()
        )

        current = (
            df_current.filter(f.col(column_name).isNotNull())
            .select(column_name)
            .cache()
        )

        # Compute quantiles on cached reference data
        reference_quantiles = reference.approxQuantile(
            column_name, self.percentiles, self.relative_error
        )
        reference_buckets = [
            -float(np.inf),
            *sorted(reference_quantiles),
            float(np.inf),
        ]

        bucketizer = Bucketizer(
            splits=reference_buckets,
            inputCol=column_name,
            outputCol=f'{self.prefix_id}_bucket',
        )

        # Transform and compute bucket counts
        reference_with_buckets = bucketizer.setHandleInvalid('keep').transform(
            reference
        )

        reference_bucket_counts = reference_with_buckets.groupBy(
            f'{self.prefix_id}_bucket'
        ).agg(f.count('*').alias(f'{self.prefix_id}_count'))

        # OPTIMIZATION 3: Calculate total from aggregated counts instead of separate count()
        reference_total_row = reference_bucket_counts.agg(
            f.sum(f'{self.prefix_id}_count').alias('total')
        ).collect()[0]
        reference_count = reference_total_row['total']

        # OPTIMIZATION 4: Remove unnecessary orderBy (order not needed for JS distance)
        reference_bucket_percentages = reference_bucket_counts.withColumn(
            f'{self.prefix_id}_percentage',
            (f.col(f'{self.prefix_id}_count') / f.lit(reference_count)),
        ).select(
            f.col(f'{self.prefix_id}_bucket'),
            f.col(f'{self.prefix_id}_percentage'),
        )

        # Process current data
        current_with_buckets = bucketizer.setHandleInvalid('keep').transform(current)

        current_bucket_counts = current_with_buckets.groupBy(
            f'{self.prefix_id}_bucket'
        ).agg(f.count('*').alias(f'{self.prefix_id}_count'))

        # OPTIMIZATION 3: Calculate total from aggregated counts
        current_total_row = current_bucket_counts.agg(
            f.sum(f'{self.prefix_id}_count').alias('total')
        ).collect()[0]
        current_count = current_total_row['total']

        # OPTIMIZATION 4: Remove unnecessary orderBy
        current_bucket_percentages = current_bucket_counts.withColumn(
            f'{self.prefix_id}_percentage',
            (f.col(f'{self.prefix_id}_count') / f.lit(current_count)),
        ).select(
            f.col(f'{self.prefix_id}_bucket'),
            f.col(f'{self.prefix_id}_percentage'),
        )

        # Unpersist cached DataFrames
        reference.unpersist()
        current.unpersist()

        return reference_bucket_percentages, current_bucket_percentages

    def __jensen_shannon_distance(
        self, column_name: str, data_type: FieldTypes
    ) -> Optional[float]:
        """Compute the Jensen-Shannon Distance according to the data type (discrete or continuous).

        Parameters:
        - column_name (str): The name of the column
        - data_type (str): The type of the field (discrete or continuous)

        Returns:
        The Jensen-Shannon value.

        """

        def align_dicts(reference_dict, current_dict):
            """Check if reference and current have the same keys.
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
            reference_dict, current_dict = (
                {key: d.get(key, 0.0) for key in all_keys} for d in dicts
            )
            return reference_dict, current_dict

        def df_to_dict(df, key_col, value_col):
            """Convert DataFrame to dictionary using native Spark collect.

            OPTIMIZATION: Replace toPandas() with native Spark operations to avoid
            driver memory issues with high-cardinality columns.

            Parameters:
            - df: DataFrame with key and value columns
            - key_col: Name of the key column
            - value_col: Name of the value column

            Returns:
            Dictionary mapping keys to values

            """
            rows = df.select(key_col, value_col).collect()
            return {row[key_col]: row[value_col] for row in rows}

        if data_type == FieldTypes.categorical:
            reference_category_percentages = self.__calculate_category_percentages(
                df=self.reference_data, column_name=column_name
            )

            current_category_percentages = self.__calculate_category_percentages(
                df=self.current_data, column_name=column_name
            )

            # OPTIMIZATION 5: Replace toPandas() with native Spark collect()
            reference_category_dict = df_to_dict(
                reference_category_percentages,
                f'{self.prefix_id}_category',
                f'{self.prefix_id}_percentage',
            )

            current_category_dict = df_to_dict(
                current_category_percentages,
                f'{self.prefix_id}_category',
                f'{self.prefix_id}_percentage',
            )

            if reference_category_dict.keys() != current_category_dict.keys():
                reference_category_dict, current_category_dict = align_dicts(
                    reference_category_dict, current_category_dict
                )

            # OPTIMIZATION 6: Use tuple instead of list for numpy array creation
            reference_values = np.array(tuple(reference_category_dict.values()))
            current_values = np.array(tuple(current_category_dict.values()))

            return float(jensenshannon(reference_values, current_values))

        reference_bucket_percentage, current_bucket_percentage = (
            self.__bucketize_continuous_values(
                df_reference=self.reference_data,
                df_current=self.current_data,
                column_name=column_name,
            )
        )

        # OPTIMIZATION 5: Replace toPandas() with native Spark collect()
        reference_bucket_dict = df_to_dict(
            reference_bucket_percentage,
            f'{self.prefix_id}_bucket',
            f'{self.prefix_id}_percentage',
        )

        current_bucket_dict = df_to_dict(
            current_bucket_percentage,
            f'{self.prefix_id}_bucket',
            f'{self.prefix_id}_percentage',
        )

        if reference_bucket_dict.keys() != current_bucket_dict.keys():
            reference_bucket_dict, current_bucket_dict = align_dicts(
                reference_bucket_dict, current_bucket_dict
            )

        # OPTIMIZATION 6: Use tuple instead of list for numpy array creation
        reference_values = np.array(tuple(reference_bucket_dict.values()))
        current_values = np.array(tuple(current_bucket_dict.values()))

        return float(jensenshannon(reference_values, current_values))

    def compute_distance(self, on_column: str, data_type: FieldTypes) -> dict:
        """Return the Jensen-Shannon Distance.

        Parameters:
        - on_column (str): The column to use for the distance computation
        - data_type (str): The type of the field (discrete or continuous)

        Returns:
        The distance as a dictionary.

        """

        return {
            'JensenShannonDistance': self.__jensen_shannon_distance(
                column_name=on_column, data_type=data_type
            )
        }
