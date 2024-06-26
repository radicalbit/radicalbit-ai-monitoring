from typing import List

import pyspark.sql.functions as f

from models.reference_dataset import ReferenceDataset
from .data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    Histogram,
    MultiClassDataQuality,
)


class ReferenceMetricsMulticlassService:
    def __init__(self, reference: ReferenceDataset):
        self.reference = reference
        index_label_map, indexed_reference = reference.get_string_indexed_dataframe()
        self.index_label_map = index_label_map
        self.indexed_reference = indexed_reference

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        numerical_features = [
            numerical.name
            for numerical in self.reference.model.get_numerical_features()
        ]

        def check_not_null(x):
            return f.when(f.col(x).isNotNull() & ~f.isnan(x), f.col(x))

        def split_dict(dictionary):
            cleaned_dict = dict()
            for k, v in dictionary.items():
                feature, metric = tuple(k.rsplit("-", 1))
                cleaned_dict.setdefault(feature, dict())[metric] = v
            return cleaned_dict

        mean_agg = [
            (f.mean(check_not_null(x))).alias(f"{x}-mean") for x in numerical_features
        ]

        max_agg = [
            (f.max(check_not_null(x))).alias(f"{x}-max") for x in numerical_features
        ]

        min_agg = [
            (f.min(check_not_null(x))).alias(f"{x}-min") for x in numerical_features
        ]

        median_agg = [
            (f.median(check_not_null(x))).alias(f"{x}-median")
            for x in numerical_features
        ]

        perc_25_agg = [
            (f.percentile(check_not_null(x), 0.25)).alias(f"{x}-perc_25")
            for x in numerical_features
        ]

        perc_75_agg = [
            (f.percentile(check_not_null(x), 0.75)).alias(f"{x}-perc_75")
            for x in numerical_features
        ]

        std_agg = [
            (f.std(check_not_null(x))).alias(f"{x}-std") for x in numerical_features
        ]

        missing_values_agg = [
            (f.count(f.when(f.col(x).isNull() | f.isnan(x), x))).alias(
                f"{x}-missing_values"
            )
            for x in numerical_features
        ]

        missing_values_perc_agg = [
            (
                (
                    f.count(f.when(f.col(x).isNull() | f.isnan(x), x))
                    / self.reference.reference_count
                )
                * 100
            ).alias(f"{x}-missing_values_perc")
            for x in numerical_features
        ]

        # Global
        global_stat = self.reference.reference.select(numerical_features).agg(
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
            column: self.reference.reference.select(column)
            .rdd.flatMap(lambda x: x)
            .histogram(10)
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
                true_feature_dict={},
                false_feature_dict={},
                histogram=dict_of_hist.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

        return numerical_features_metrics

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        categorical_features = [
            categorical.name
            for categorical in self.reference.model.get_categorical_features()
        ]

        def check_not_null(x):
            return f.when(f.col(x).isNotNull(), f.col(x))

        def split_dict(dictionary):
            cleaned_dict = dict()
            for k, v in dictionary.items():
                feature, metric = tuple(k.rsplit("-", 1))
                cleaned_dict.setdefault(feature, dict())[metric] = v
            return cleaned_dict

        missing_values_agg = [
            (f.count(f.when(f.col(x).isNull(), x))).alias(f"{x}-missing_values")
            for x in categorical_features
        ]

        missing_values_perc_agg = [
            (
                (f.count(f.when(f.col(x).isNull(), x)) / self.reference.reference_count)
                * 100
            ).alias(f"{x}-missing_values_perc")
            for x in categorical_features
        ]

        distinct_values = [
            (f.countDistinct(check_not_null(x))).alias(f"{x}-distinct_values")
            for x in categorical_features
        ]

        global_stat = self.reference.reference.select(categorical_features).agg(
            *(missing_values_agg + missing_values_perc_agg + distinct_values)
        )

        global_dict = global_stat.toPandas().iloc[0].to_dict()
        global_data_quality = split_dict(global_dict)

        # FIXME by design this is not efficient
        # FIXME understand if we want to divide by whole or by number of not null

        count_distinct_categories = {
            column: dict(
                self.reference.reference.select(column)
                .filter(f.isnotnull(column))
                .groupBy(column)
                .agg(*[f.count(check_not_null(column)).alias("count")])
                .withColumn(
                    "freq",
                    f.col("count") / self.reference.reference_count,
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

    def calculate_class_metrics(self) -> List[ClassMetrics]:
        def check_not_null(x):
            return f.when(f.col(x).isNotNull(), f.col(x))

        class_metrics_dict = (
            self.reference.reference.select(
                self.reference.model.outputs.prediction.name
            )
            .filter(f.isnotnull(self.reference.model.outputs.prediction.name))
            .groupBy(self.reference.model.outputs.prediction.name)
            .agg(
                *[
                    f.count(
                        check_not_null(self.reference.model.outputs.prediction.name)
                    ).alias("count")
                ]
            )
            .withColumn(
                "percentage",
                (f.col("count") / self.reference.reference_count) * 100,
            )
            .toPandas()
            .set_index(self.reference.model.outputs.prediction.name)
            .to_dict(orient="index")
        )

        return [
            ClassMetrics(
                name=label,
                count=metrics["count"],
                percentage=metrics["percentage"],
            )
            for label, metrics in class_metrics_dict.items()
        ]

    def calculate_data_quality(self) -> MultiClassDataQuality:
        feature_metrics = []
        if self.reference.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.reference.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return MultiClassDataQuality(
            n_observations=self.reference.reference_count,
            class_metrics=self.calculate_class_metrics(),
            feature_metrics=feature_metrics,
        )
