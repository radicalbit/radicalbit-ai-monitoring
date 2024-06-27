from typing import List

import pyspark.sql.functions as F
from pandas import DataFrame

from models.data_quality import (
    NumericalFeatureMetrics,
    Histogram,
    CategoricalFeatureMetrics,
    ClassMetrics,
)
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
        model: ModelOut, dataframe: DataFrame, dataframe_count: int
    ) -> List[ClassMetrics]:
        class_metrics_dict = (
            dataframe.select(model.outputs.prediction.name)
            .filter(F.isnotnull(model.outputs.prediction.name))
            .groupBy(model.outputs.prediction.name)
            .agg(
                *[F.count(check_not_null(model.outputs.prediction.name)).alias("count")]
            )
            .withColumn(
                "percentage",
                (F.col("count") / dataframe_count) * 100,
            )
            .toPandas()
            .set_index(model.outputs.prediction.name)
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
