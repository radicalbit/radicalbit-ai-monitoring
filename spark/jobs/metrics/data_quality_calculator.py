from math import inf
from typing import Dict, List

from models.data_quality import (
    CategoricalFeatureMetrics,
    ClassMetrics,
    Histogram,
    NumericalFeatureMetrics,
    NumericalTargetMetrics,
)
import numpy as np
from pandas import DataFrame
from pyspark.ml.feature import Bucketizer
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType
from utils.misc import split_dict
from utils.models import ModelOut
from utils.spark import check_not_null


class DataQualityCalculator:
    @staticmethod
    def numerical_metrics(
        model: ModelOut, dataframe: DataFrame, dataframe_count: int
    ) -> List[NumericalFeatureMetrics]:
        numerical_features = [
            numerical.name for numerical in model.get_numerical_features()
        ]

        mean_agg = [
            (F.mean(check_not_null(x))).alias(f'{x}-mean') for x in numerical_features
        ]

        max_agg = [
            (F.max(check_not_null(x))).alias(f'{x}-max') for x in numerical_features
        ]

        min_agg = [
            (F.min(check_not_null(x))).alias(f'{x}-min') for x in numerical_features
        ]

        median_agg = [
            (F.median(check_not_null(x))).alias(f'{x}-median')
            for x in numerical_features
        ]

        perc_25_agg = [
            (F.percentile(check_not_null(x), 0.25)).alias(f'{x}-perc_25')
            for x in numerical_features
        ]

        perc_75_agg = [
            (F.percentile(check_not_null(x), 0.75)).alias(f'{x}-perc_75')
            for x in numerical_features
        ]

        std_agg = [
            (F.std(check_not_null(x))).alias(f'{x}-std') for x in numerical_features
        ]

        missing_values_agg = [
            (F.count(F.when(F.col(x).isNull() | F.isnan(x), x))).alias(
                f'{x}-missing_values'
            )
            for x in numerical_features
        ]

        missing_values_perc_agg = [
            (
                (F.count(F.when(F.col(x).isNull() | F.isnan(x), x)) / dataframe_count)
                * 100
            ).alias(f'{x}-missing_values_perc')
            for x in numerical_features
        ]

        # Global
        global_stat = dataframe.select(numerical_features).agg(
            *(
                mean_agg
                + max_agg
                + min_agg
                + median_agg
                + perc_25_agg
                + perc_75_agg
                + std_agg
                + missing_values_agg
                + missing_values_perc_agg
            )
        )

        # ✅ OPTIMIZATION: Direct conversion without pandas overhead
        global_dict = global_stat.first().asDict()
        global_data_quality = split_dict(global_dict)

        # ✅ OPTIMIZATION: Use DataFrame API instead of RDD for histograms
        # Calculate min/max for all columns in a single pass
        min_max_exprs = []
        for column in numerical_features:
            min_max_exprs.append(F.min(column).alias(f'{column}_min'))
            min_max_exprs.append(F.max(column).alias(f'{column}_max'))

        min_max_result = (
            dataframe.select(numerical_features).agg(*min_max_exprs).first().asDict()
        )

        # Generate histograms using DataFrame API
        histograms = {}
        for column in numerical_features:
            min_val = min_max_result[f'{column}_min']
            max_val = min_max_result[f'{column}_max']

            if min_val is None or max_val is None:
                # Handle all-null columns
                histograms[column] = ([0.0] * 11, [0] * 10)
                continue

            # Generate bucket boundaries
            if min_val == max_val:
                # All values are the same
                buckets = [min_val - 0.5, min_val + 0.5]
                counts = [dataframe.filter(F.col(column).isNotNull()).count()]
            else:
                buckets = np.linspace(min_val, max_val, 11).tolist()

                # Use Bucketizer for efficient histogram calculation
                bucketizer = Bucketizer(
                    splits=buckets, inputCol=column, outputCol=f'{column}_bucket'
                )
                bucketed = bucketizer.setHandleInvalid('skip').transform(
                    dataframe.select(column)
                )

                # Count values in each bucket
                bucket_counts = (
                    bucketed.groupBy(f'{column}_bucket')
                    .count()
                    .orderBy(f'{column}_bucket')
                    .select('count')
                    .collect()
                )
                counts = [row['count'] for row in bucket_counts]

                # Ensure we have exactly 10 buckets
                while len(counts) < 10:
                    counts.append(0)

            histograms[column] = (buckets, counts)

        dict_of_hist = {
            k: Histogram(buckets=v[0], reference_values=v[1])
            for k, v in histograms.items()
        }

        return [
            NumericalFeatureMetrics.from_dict(
                feature_name,
                metrics,
                histogram=dict_of_hist.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

    @staticmethod
    def categorical_metrics(
        model: ModelOut, dataframe: DataFrame, dataframe_count: int, prefix_id: str
    ) -> List[CategoricalFeatureMetrics]:
        categorical_features = [
            categorical.name for categorical in model.get_categorical_features()
        ]

        missing_values_agg = [
            (F.count(F.when(F.col(x).isNull(), x))).alias(f'{x}-missing_values')
            for x in categorical_features
        ]

        missing_values_perc_agg = [
            ((F.count(F.when(F.col(x).isNull(), x)) / dataframe_count) * 100).alias(
                f'{x}-missing_values_perc'
            )
            for x in categorical_features
        ]

        distinct_values = [
            (F.countDistinct(check_not_null(x))).alias(f'{x}-distinct_values')
            for x in categorical_features
        ]

        global_stat = dataframe.select(categorical_features).agg(
            *(missing_values_agg + missing_values_perc_agg + distinct_values)
        )

        # ✅ OPTIMIZATION: Direct conversion without pandas overhead
        global_dict = global_stat.first().asDict()
        global_data_quality = split_dict(global_dict)

        # ✅ OPTIMIZATION: Single query for all categorical features instead of N queries
        # Unpivot all categorical columns and compute counts in one pass
        if categorical_features:
            # Create expressions for unpivoting
            stack_expr = ', '.join([f"'{col}', {col}" for col in categorical_features])

            unpivoted = dataframe.selectExpr(
                f'stack({len(categorical_features)}, {stack_expr}) as (feature_name, feature_value)'
            ).filter(F.col('feature_value').isNotNull())

            # Calculate counts and frequencies for all features in single aggregation
            category_stats = (
                unpivoted.groupBy('feature_name', 'feature_value')
                .agg(F.count('*').alias(f'{prefix_id}_count'))
                .withColumn(
                    f'{prefix_id}_freq', F.col(f'{prefix_id}_count') / dataframe_count
                )
                .orderBy('feature_name', 'feature_value')  # Ensure consistent ordering
                .collect()
            )

            # Organize results by feature - match original structure exactly
            count_distinct_categories = {}
            for row in category_stats:
                feature = row['feature_name']
                value = row['feature_value']

                if feature not in count_distinct_categories:
                    count_distinct_categories[feature] = {
                        f'{prefix_id}_count': {},
                        f'{prefix_id}_freq': {},
                    }

                count_distinct_categories[feature][f'{prefix_id}_count'][value] = row[
                    f'{prefix_id}_count'
                ]
                count_distinct_categories[feature][f'{prefix_id}_freq'][value] = row[
                    f'{prefix_id}_freq'
                ]
        else:
            count_distinct_categories = {}

        return [
            CategoricalFeatureMetrics.from_dict(
                feature_name=feature_name,
                global_metrics=metrics,
                categories_metrics=count_distinct_categories.get(feature_name),
                prefix_id=prefix_id,
            )
            for feature_name, metrics in global_data_quality.items()
        ]

    @staticmethod
    def class_metrics(
        class_column: str, dataframe: DataFrame, dataframe_count: int, prefix_id: str
    ) -> List[ClassMetrics]:
        class_metrics_dict = (
            dataframe.select(class_column)
            .filter(F.isnotnull(class_column))
            .groupBy(class_column)
            .agg(*[F.count(check_not_null(class_column)).alias(f'{prefix_id}_count')])
            .orderBy(class_column)
            .withColumn(
                f'{prefix_id}_percentage',
                (F.col(f'{prefix_id}_count') / dataframe_count) * 100,
            )
            .toPandas()
            .set_index(class_column)
            .to_dict(orient='index')
        )
        return [
            ClassMetrics(
                name=str(label),
                count=metrics[f'{prefix_id}_count'],
                percentage=metrics[f'{prefix_id}_percentage'],
            )
            for label, metrics in class_metrics_dict.items()
        ]

    @staticmethod
    def calculate_combined_histogram(
        current_dataframe: DataFrame,
        reference_dataframe: DataFrame,
        spark_session: SparkSession,
        columns: List[str],
        prefix_id: str,
    ) -> Dict[str, Histogram]:
        current = current_dataframe.withColumn(f'{prefix_id}_type', F.lit('current'))
        reference = reference_dataframe.withColumn(
            f'{prefix_id}_type', F.lit('reference')
        )

        def create_histogram(feature: str):
            reference_and_current = current.select(
                [feature, f'{prefix_id}_type']
            ).unionByName(reference.select([feature, f'{prefix_id}_type']))

            # ✅ OPTIMIZATION: Single aggregation for both min and max
            min_max_result = reference_and_current.agg(
                F.min(
                    F.when(
                        F.col(feature).isNotNull() & ~F.isnan(feature),
                        F.col(feature),
                    )
                ).alias('min_value'),
                F.max(
                    F.when(
                        F.col(feature).isNotNull() & ~F.isnan(feature),
                        F.col(feature),
                    )
                ).alias('max_value'),
            ).first()

            max_value = min_max_result['max_value']
            min_value = min_max_result['min_value']

            buckets_spacing = np.linspace(min_value, max_value, 11).tolist()
            lookup = set()
            generated_buckets = [
                x for x in buckets_spacing if x not in lookup and lookup.add(x) is None
            ]
            # workaround if all values are the same to not have errors
            if len(generated_buckets) == 1:
                buckets_spacing = [generated_buckets[0], generated_buckets[0]]
                buckets = [-float(inf), generated_buckets[0], float(inf)]
            else:
                buckets = generated_buckets

            bucketizer = Bucketizer(
                splits=buckets, inputCol=feature, outputCol='bucket'
            )
            result = bucketizer.setHandleInvalid('keep').transform(
                reference_and_current
            )

            current_df = (
                result.filter(F.col(f'{prefix_id}_type') == 'current')
                .groupBy('bucket')
                .agg(F.count(F.col(feature)).alias('curr_count'))
            )
            reference_df = (
                result.filter(F.col(f'{prefix_id}_type') == 'reference')
                .groupBy('bucket')
                .agg(F.count(F.col(feature)).alias('ref_count'))
            )

            buckets_number = list(range(10))
            bucket_df = spark_session.createDataFrame(
                buckets_number, IntegerType()
            ).withColumnRenamed('value', 'bucket')
            tot_df = (
                bucket_df.join(current_df, on=['bucket'], how='left')
                .join(reference_df, on=['bucket'], how='left')
                .fillna(0)
                .orderBy('bucket')
            )
            # workaround if all values are the same to not have errors
            if len(generated_buckets) == 1:
                tot_df = tot_df.filter(F.col('bucket') == 1)

            # ✅ OPTIMIZATION: Use DataFrame API instead of RDD
            collected_data = tot_df.select('curr_count', 'ref_count').collect()
            cur = [row['curr_count'] for row in collected_data]
            ref = [row['ref_count'] for row in collected_data]

            return Histogram(
                buckets=buckets_spacing, reference_values=ref, current_values=cur
            )

        return {feature: create_histogram(feature) for feature in columns}

    @staticmethod
    def calculate_combined_data_quality_numerical(
        model: ModelOut,
        current_dataframe: DataFrame,
        current_count: int,
        reference_dataframe: DataFrame,
        spark_session: SparkSession,
        prefix_id: str,
    ) -> List[NumericalFeatureMetrics]:
        numerical_features = [
            numerical.name for numerical in model.get_numerical_features()
        ]

        mean_agg = [
            (F.mean(check_not_null(x))).alias(f'{x}-mean') for x in numerical_features
        ]

        max_agg = [
            (F.max(check_not_null(x))).alias(f'{x}-max') for x in numerical_features
        ]

        min_agg = [
            (F.min(check_not_null(x))).alias(f'{x}-min') for x in numerical_features
        ]

        median_agg = [
            (F.median(check_not_null(x))).alias(f'{x}-median')
            for x in numerical_features
        ]

        perc_25_agg = [
            (F.percentile(check_not_null(x), 0.25)).alias(f'{x}-perc_25')
            for x in numerical_features
        ]

        perc_75_agg = [
            (F.percentile(check_not_null(x), 0.75)).alias(f'{x}-perc_75')
            for x in numerical_features
        ]

        std_agg = [
            (F.std(check_not_null(x))).alias(f'{x}-std') for x in numerical_features
        ]

        missing_values_agg = [
            (F.count(F.when(F.col(x).isNull() | F.isnan(x), x))).alias(
                f'{x}-missing_values'
            )
            for x in numerical_features
        ]

        missing_values_perc_agg = [
            (
                (F.count(F.when(F.col(x).isNull() | F.isnan(x), x)) / current_count)
                * 100
            ).alias(f'{x}-missing_values_perc')
            for x in numerical_features
        ]

        # Global
        global_stat = current_dataframe.select(numerical_features).agg(
            *(
                mean_agg
                + max_agg
                + min_agg
                + median_agg
                + perc_25_agg
                + perc_75_agg
                + std_agg
                + missing_values_agg
                + missing_values_perc_agg
            )
        )

        # ✅ OPTIMIZATION: Direct conversion without pandas overhead
        global_dict = global_stat.first().asDict()
        global_data_quality = split_dict(global_dict)

        numerical_features_histogram = (
            DataQualityCalculator.calculate_combined_histogram(
                current_dataframe,
                reference_dataframe,
                spark_session,
                numerical_features,
                prefix_id,
            )
        )

        return [
            NumericalFeatureMetrics.from_dict(
                feature_name,
                metrics,
                histogram=numerical_features_histogram.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

    @staticmethod
    def regression_target_metrics(
        target_column: str, dataframe: DataFrame, dataframe_count: int
    ) -> NumericalTargetMetrics:
        target_metrics = DataQualityCalculator.regression_target_metrics_for_dataframe(
            target_column, dataframe, dataframe_count
        )

        # ✅ OPTIMIZATION: Use DataFrame API instead of RDD for histogram
        min_max_result = dataframe.select(
            F.min(target_column).alias('min_val'), F.max(target_column).alias('max_val')
        ).first()

        min_val = min_max_result['min_val']
        max_val = min_max_result['max_val']

        if min_val is None or max_val is None:
            histogram = Histogram(buckets=[0.0] * 11, reference_values=[0] * 10)
        elif min_val == max_val:
            buckets = [min_val - 0.5, min_val + 0.5]
            counts = [dataframe.filter(F.col(target_column).isNotNull()).count()]
            histogram = Histogram(buckets=buckets, reference_values=counts)
        else:
            buckets = np.linspace(min_val, max_val, 11).tolist()
            bucketizer = Bucketizer(
                splits=buckets,
                inputCol=target_column,
                outputCol=f'{target_column}_bucket',
            )
            bucketed = bucketizer.setHandleInvalid('skip').transform(
                dataframe.select(target_column)
            )
            bucket_counts = (
                bucketed.groupBy(f'{target_column}_bucket')
                .count()
                .orderBy(f'{target_column}_bucket')
                .select('count')
                .collect()
            )
            counts = [row['count'] for row in bucket_counts]
            while len(counts) < 10:
                counts.append(0)
            histogram = Histogram(buckets=buckets, reference_values=counts)

        return NumericalTargetMetrics.from_dict(
            target_column, target_metrics, histogram
        )

    @staticmethod
    def regression_target_metrics_current(
        target_column: str,
        curr_df: DataFrame,
        curr_count: int,
        ref_df: DataFrame,
        spark_session: SparkSession,
        prefix_id: str,
    ):
        target_metrics = DataQualityCalculator.regression_target_metrics_for_dataframe(
            target_column, curr_df, curr_count
        )
        _histogram = DataQualityCalculator.calculate_combined_histogram(
            curr_df, ref_df, spark_session, [target_column], prefix_id
        )
        histogram = _histogram[target_column]

        return NumericalTargetMetrics.from_dict(
            target_column, target_metrics, histogram
        )

    @staticmethod
    def regression_target_metrics_for_dataframe(
        target_column: str, dataframe: DataFrame, dataframe_count: int
    ) -> dict:
        result = (
            dataframe.select(target_column)
            .filter(F.isnotnull(target_column))
            .agg(
                F.mean(target_column).alias('mean'),
                F.stddev(target_column).alias('std'),
                F.max(target_column).alias('max'),
                F.min(target_column).alias('min'),
                F.median(target_column).alias('median'),
                F.percentile_approx(target_column, 0.25).alias('perc_25'),
                F.percentile_approx(target_column, 0.75).alias('perc_75'),
                F.count(F.when(F.col(target_column).isNull(), target_column)).alias(
                    'missing_values'
                ),
                (
                    (
                        F.count(
                            F.when(
                                F.col(target_column).isNull() | F.isnan(target_column),
                                target_column,
                            )
                        )
                        / dataframe_count
                    )
                    * 100
                ).alias('missing_values_perc'),
            )
        )

        # ✅ OPTIMIZATION: Direct conversion without pandas overhead
        return result.first().asDict()
