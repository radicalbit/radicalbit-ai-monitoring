from math import inf
from typing import List, Dict

import numpy as np
import pyspark.sql.functions as F
from pandas import DataFrame
from pyspark.ml.feature import Bucketizer
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType

from models.data_quality import (
    NumericalFeatureMetrics,
    Histogram,
    CategoricalFeatureMetrics,
    ClassMetrics,
    NumericalTargetMetrics,
)
from utils.misc import split_dict, rbit_prefix
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
            (F.mean(check_not_null(x))).alias(f"{x}-mean") for x in numerical_features
        ]

        max_agg = [
            (F.max(check_not_null(x))).alias(f"{x}-max") for x in numerical_features
        ]

        min_agg = [
            (F.min(check_not_null(x))).alias(f"{x}-min") for x in numerical_features
        ]

        median_agg = [
            (F.median(check_not_null(x))).alias(f"{x}-median")
            for x in numerical_features
        ]

        perc_25_agg = [
            (F.percentile(check_not_null(x), 0.25)).alias(f"{x}-perc_25")
            for x in numerical_features
        ]

        perc_75_agg = [
            (F.percentile(check_not_null(x), 0.75)).alias(f"{x}-perc_75")
            for x in numerical_features
        ]

        std_agg = [
            (F.std(check_not_null(x))).alias(f"{x}-std") for x in numerical_features
        ]

        missing_values_agg = [
            (F.count(F.when(F.col(x).isNull() | F.isnan(x), x))).alias(
                f"{x}-missing_values"
            )
            for x in numerical_features
        ]

        missing_values_perc_agg = [
            (
                (F.count(F.when(F.col(x).isNull() | F.isnan(x), x)) / dataframe_count)
                * 100
            ).alias(f"{x}-missing_values_perc")
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

        global_dict = global_stat.toPandas().iloc[0].to_dict()
        global_data_quality = split_dict(global_dict)

        # TODO probably not so efficient but I haven't found another way
        histograms = {
            column: dataframe.select(column).rdd.flatMap(lambda x: x).histogram(10)
            for column in numerical_features
        }

        dict_of_hist = {
            k: Histogram(buckets=v[0], reference_values=v[1])
            for k, v in histograms.items()
        }

        numerical_features_metrics = [
            NumericalFeatureMetrics.from_dict(
                feature_name,
                metrics,
                histogram=dict_of_hist.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

        return numerical_features_metrics

    @staticmethod
    def categorical_metrics(
        model: ModelOut, dataframe: DataFrame, dataframe_count: int
    ) -> List[CategoricalFeatureMetrics]:
        categorical_features = [
            categorical.name for categorical in model.get_categorical_features()
        ]

        missing_values_agg = [
            (F.count(F.when(F.col(x).isNull(), x))).alias(f"{x}-missing_values")
            for x in categorical_features
        ]

        missing_values_perc_agg = [
            ((F.count(F.when(F.col(x).isNull(), x)) / dataframe_count) * 100).alias(
                f"{x}-missing_values_perc"
            )
            for x in categorical_features
        ]

        distinct_values = [
            (F.countDistinct(check_not_null(x))).alias(f"{x}-distinct_values")
            for x in categorical_features
        ]

        global_stat = dataframe.select(categorical_features).agg(
            *(missing_values_agg + missing_values_perc_agg + distinct_values)
        )

        global_dict = global_stat.toPandas().iloc[0].to_dict()
        global_data_quality = split_dict(global_dict)

        # FIXME by design this is not efficient
        # FIXME understand if we want to divide by whole or by number of not null

        count_distinct_categories = {
            column: dict(
                dataframe.select(column)
                .filter(F.isnotnull(column))
                .groupBy(column)
                .agg(*[F.count(check_not_null(column)).alias("count")])
                .withColumn(
                    "freq",
                    F.col("count") / dataframe_count,
                )
                .toPandas()
                .set_index(column)
                .to_dict()
            )
            for column in categorical_features
        }

        categorical_features_metrics = [
            CategoricalFeatureMetrics.from_dict(
                feature_name=feature_name,
                global_metrics=metrics,
                categories_metrics=count_distinct_categories.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

        return categorical_features_metrics

    @staticmethod
    def class_metrics(
        class_column: str, dataframe: DataFrame, dataframe_count: int
    ) -> List[ClassMetrics]:
        class_metrics_dict = (
            dataframe.select(class_column)
            .filter(F.isnotnull(class_column))
            .groupBy(class_column)
            .agg(*[F.count(check_not_null(class_column)).alias("count")])
            .orderBy(class_column)
            .withColumn(
                "percentage",
                (F.col("count") / dataframe_count) * 100,
            )
            .toPandas()
            .set_index(class_column)
            .to_dict(orient="index")
        )

        return [
            ClassMetrics(
                name=str(label),
                count=metrics["count"],
                percentage=metrics["percentage"],
            )
            for label, metrics in class_metrics_dict.items()
        ]

    @staticmethod
    def calculate_combined_histogram(
        current_dataframe: DataFrame,
        reference_dataframe: DataFrame,
        spark_session: SparkSession,
        columns: List[str],
    ) -> Dict[str, Histogram]:
        current = current_dataframe.withColumn(f"{rbit_prefix}type", F.lit("current"))
        reference = reference_dataframe.withColumn(
            f"{rbit_prefix}type", F.lit("reference")
        )

        def create_histogram(feature: str):
            reference_and_current = current.select(
                [feature, f"{rbit_prefix}type"]
            ).unionByName(reference.select([feature, f"{rbit_prefix}type"]))

            max_value = reference_and_current.agg(
                F.max(
                    F.when(
                        F.col(feature).isNotNull() & ~F.isnan(feature),
                        F.col(feature),
                    )
                )
            ).collect()[0][0]
            min_value = reference_and_current.agg(
                F.min(
                    F.when(
                        F.col(feature).isNotNull() & ~F.isnan(feature),
                        F.col(feature),
                    )
                )
            ).collect()[0][0]

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
                splits=buckets, inputCol=feature, outputCol="bucket"
            )
            result = bucketizer.setHandleInvalid("keep").transform(
                reference_and_current
            )

            current_df = (
                result.filter(F.col(f"{rbit_prefix}type") == "current")
                .groupBy("bucket")
                .agg(F.count(F.col(feature)).alias("curr_count"))
            )
            reference_df = (
                result.filter(F.col(f"{rbit_prefix}type") == "reference")
                .groupBy("bucket")
                .agg(F.count(F.col(feature)).alias("ref_count"))
            )

            buckets_number = list(range(10))
            bucket_df = spark_session.createDataFrame(
                buckets_number, IntegerType()
            ).withColumnRenamed("value", "bucket")
            tot_df = (
                bucket_df.join(current_df, on=["bucket"], how="left")
                .join(reference_df, on=["bucket"], how="left")
                .fillna(0)
                .orderBy("bucket")
            )
            # workaround if all values are the same to not have errors
            if len(generated_buckets) == 1:
                tot_df = tot_df.filter(F.col("bucket") == 1)
            cur = tot_df.select("curr_count").rdd.flatMap(lambda x: x).collect()
            ref = tot_df.select("ref_count").rdd.flatMap(lambda x: x).collect()
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
    ) -> List[NumericalFeatureMetrics]:
        numerical_features = [
            numerical.name for numerical in model.get_numerical_features()
        ]

        mean_agg = [
            (F.mean(check_not_null(x))).alias(f"{x}-mean") for x in numerical_features
        ]

        max_agg = [
            (F.max(check_not_null(x))).alias(f"{x}-max") for x in numerical_features
        ]

        min_agg = [
            (F.min(check_not_null(x))).alias(f"{x}-min") for x in numerical_features
        ]

        median_agg = [
            (F.median(check_not_null(x))).alias(f"{x}-median")
            for x in numerical_features
        ]

        perc_25_agg = [
            (F.percentile(check_not_null(x), 0.25)).alias(f"{x}-perc_25")
            for x in numerical_features
        ]

        perc_75_agg = [
            (F.percentile(check_not_null(x), 0.75)).alias(f"{x}-perc_75")
            for x in numerical_features
        ]

        std_agg = [
            (F.std(check_not_null(x))).alias(f"{x}-std") for x in numerical_features
        ]

        missing_values_agg = [
            (F.count(F.when(F.col(x).isNull() | F.isnan(x), x))).alias(
                f"{x}-missing_values"
            )
            for x in numerical_features
        ]

        missing_values_perc_agg = [
            (
                (F.count(F.when(F.col(x).isNull() | F.isnan(x), x)) / current_count)
                * 100
            ).alias(f"{x}-missing_values_perc")
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

        global_dict = global_stat.toPandas().iloc[0].to_dict()
        global_data_quality = split_dict(global_dict)

        numerical_features_histogram = (
            DataQualityCalculator.calculate_combined_histogram(
                current_dataframe,
                reference_dataframe,
                spark_session,
                numerical_features,
            )
        )

        numerical_features_metrics = [
            NumericalFeatureMetrics.from_dict(
                feature_name,
                metrics,
                histogram=numerical_features_histogram.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

        return numerical_features_metrics

    def regression_target_metrics(
        target_column: str, dataframe: DataFrame, dataframe_count: int
    ) -> NumericalTargetMetrics:
        target_metrics = DataQualityCalculator.regression_target_metrics_for_dataframe(
            target_column, dataframe, dataframe_count
        )

        _histogram = (
            dataframe.select(target_column).rdd.flatMap(lambda x: x).histogram(10)
        )
        histogram = Histogram(buckets=_histogram[0], reference_values=_histogram[1])

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
    ):
        target_metrics = DataQualityCalculator.regression_target_metrics_for_dataframe(
            target_column, curr_df, curr_count
        )
        _histogram = DataQualityCalculator.calculate_combined_histogram(
            curr_df, ref_df, spark_session, [target_column]
        )
        histogram = _histogram[target_column]

        return NumericalTargetMetrics.from_dict(
            target_column, target_metrics, histogram
        )

    @staticmethod
    def regression_target_metrics_for_dataframe(
        target_column: str, dataframe: DataFrame, dataframe_count: int
    ) -> dict:
        return (
            dataframe.select(target_column)
            .filter(F.isnotnull(target_column))
            .agg(
                F.mean(target_column).alias("mean"),
                F.stddev(target_column).alias("std"),
                F.max(target_column).alias("max"),
                F.min(target_column).alias("min"),
                F.median(target_column).alias("median"),
                F.percentile_approx(target_column, 0.25).alias("perc_25"),
                F.percentile_approx(target_column, 0.75).alias("perc_75"),
                F.count(F.when(F.col(target_column).isNull(), target_column)).alias(
                    "missing_values"
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
                ).alias("missing_values_perc"),
            )
            .toPandas()
            .iloc[0]
            .to_dict()
        )
