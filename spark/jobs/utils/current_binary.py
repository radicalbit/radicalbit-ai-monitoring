from typing import List, Dict

import numpy as np
from numpy import inf
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator,
)
from pyspark.ml.feature import Bucketizer
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as f
from pyspark.sql.types import IntegerType

from metrics.data_quality_calculator import DataQualityCalculator
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    BinaryClassDataQuality,
    Histogram,
)
from .models import ModelOut, Granularity
from .ks import KolmogorovSmirnovTest
from .chi2 import Chi2Test


class CurrentMetricsService:
    # Statistics
    N_VARIABLES = "n_variables"
    N_OBSERVATION = "n_observations"
    MISSING_CELLS = "missing_cells"
    MISSING_CELLS_PERC = "missing_cells_perc"
    DUPLICATE_ROWS = "duplicate_rows"
    DUPLICATE_ROWS_PERC = "duplicate_rows_perc"
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    DATETIME = "datetime"

    # Model Quality
    model_quality_binary_classificator = {
        "areaUnderROC": "area_under_roc",
        "areaUnderPR": "area_under_pr",
    }

    model_quality_multiclass_classificator = {
        "f1": "f1",
        "accuracy": "accuracy",
        "weightedPrecision": "weighted_precision",
        "weightedRecall": "weighted_recall",
        "weightedTruePositiveRate": "weighted_true_positive_rate",
        "weightedFalsePositiveRate": "weighted_false_positive_rate",
        "weightedFMeasure": "weighted_f_measure",
        "truePositiveRateByLabel": "true_positive_rate",
        "falsePositiveRateByLabel": "false_positive_rate",
        "precisionByLabel": "precision",
        "recallByLabel": "recall",
        "fMeasureByLabel": "f_measure",
    }

    def __init__(
        self,
        spark_session: SparkSession,
        current: DataFrame,
        reference: DataFrame,
        model: ModelOut,
    ):
        self.spark_session = spark_session
        self.current = current
        self.reference = reference
        self.current_count = self.current.count()
        self.reference_count = self.reference.count()
        self.model = model

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        numerical_features = [
            numerical.name for numerical in self.model.get_numerical_features()
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
                    / self.current_count
                )
                * 100
            ).alias(f"{x}-missing_values_perc")
            for x in numerical_features
        ]

        # Global
        global_stat = self.current.select(numerical_features).agg(
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

        numerical_features_histogram = self.calculate_combined_histogram()

        numerical_features_metrics = [
            NumericalFeatureMetrics.from_dict(
                feature_name,
                metrics,
                histogram=numerical_features_histogram.get(feature_name),
            )
            for feature_name, metrics in global_data_quality.items()
        ]

        return numerical_features_metrics

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        return DataQualityCalculator.categorical_metrics(
            model=self.model, dataframe=self.current, dataframe_count=self.current_count
        )

    def calculate_class_metrics(self) -> List[ClassMetrics]:
        metrics = DataQualityCalculator.class_metrics(
            class_column=self.model.target.name,
            dataframe=self.current,
            dataframe_count=self.current_count,
        )

        # FIXME this should be avoided if we are sure that we have all classes in the file

        if len(metrics) == 1:
            if metrics[0].name == "1.0":
                return metrics + [
                    ClassMetrics(
                        name="0.0",
                        count=0,
                        percentage=0.0,
                    )
                ]
            else:
                return metrics + [
                    ClassMetrics(
                        name="1.0",
                        count=0,
                        percentage=0.0,
                    )
                ]
        else:
            return metrics

    def calculate_data_quality(self) -> BinaryClassDataQuality:
        feature_metrics = []
        if self.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return BinaryClassDataQuality(
            n_observations=self.current_count,
            class_metrics=self.calculate_class_metrics(),
            feature_metrics=feature_metrics,
        )

    def calculate_combined_histogram(self) -> Dict[str, Histogram]:
        numerical_features = [
            numerical.name for numerical in self.model.get_numerical_features()
        ]
        current = self.current.withColumn("type", f.lit("current"))
        reference = self.reference.withColumn("type", f.lit("reference"))

        def create_histogram(feature: str):
            reference_and_current = current.select([feature, "type"]).unionByName(
                reference.select([feature, "type"])
            )

            max_value = reference_and_current.agg(
                f.max(
                    f.when(
                        f.col(feature).isNotNull() & ~f.isnan(feature), f.col(feature)
                    )
                )
            ).collect()[0][0]
            min_value = reference_and_current.agg(
                f.min(
                    f.when(
                        f.col(feature).isNotNull() & ~f.isnan(feature), f.col(feature)
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
                result.filter(f.col("type") == "current")
                .groupBy("bucket")
                .agg(f.count(f.col(feature)).alias("curr_count"))
            )
            reference_df = (
                result.filter(f.col("type") == "reference")
                .groupBy("bucket")
                .agg(f.count(f.col(feature)).alias("ref_count"))
            )

            buckets_number = list(range(10))
            bucket_df = self.spark_session.createDataFrame(
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
                tot_df = tot_df.filter(f.col("bucket") == 1)
            cur = tot_df.select("curr_count").rdd.flatMap(lambda x: x).collect()
            ref = tot_df.select("ref_count").rdd.flatMap(lambda x: x).collect()
            return Histogram(
                buckets=buckets_spacing, reference_values=ref, current_values=cur
            )

        return {feature: create_histogram(feature) for feature in numerical_features}

    # FIXME use pydantic struct like data quality
    def __calc_bc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_binary_classification(self.current, name)
            for (name, label) in self.model_quality_binary_classificator.items()
        }

    # FIXME use pydantic struct like data quality
    def __calc_mc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_multi_class_classification(self.current, name)
            for (name, label) in self.model_quality_multiclass_classificator.items()
        }

    def __evaluate_binary_classification(
        self, dataset: DataFrame, metric_name: str
    ) -> float:
        try:
            return BinaryClassificationEvaluator(
                metricName=metric_name,
                labelCol=self.model.target.name,
                rawPredictionCol=self.model.outputs.prediction_proba.name,
            ).evaluate(dataset)
        except Exception:
            return float("nan")

    def __evaluate_multi_class_classification(
        self, dataset: DataFrame, metric_name: str
    ) -> float:
        # metricLabel=1 is required otherwise this will take 0 as the positive label, with errors in calculations
        # because this is used as binary classificator even if it is a multiclass
        try:
            return MulticlassClassificationEvaluator(
                metricName=metric_name,
                predictionCol=self.model.outputs.prediction.name,
                labelCol=self.model.target.name,
                metricLabel=1,
            ).evaluate(dataset)
        except Exception:
            return float("nan")

    def calculate_multiclass_model_quality_group_by_timestamp(self):
        def create_time_format(granularity: Granularity):
            match granularity:
                case Granularity.HOUR:
                    return "yyyy-MM-dd HH"
                case Granularity.DAY:
                    return "yyyy-MM-dd"
                case Granularity.WEEK:
                    return "yyyy-MM-dd"
                case Granularity.MONTH:
                    return "yyyy-MM"

        if self.model.granularity == Granularity.WEEK:
            dataset_with_group = self.current.select(
                [
                    self.model.outputs.prediction.name,
                    self.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_sub(
                                f.next_day(
                                    f.date_format(
                                        self.model.timestamp.name,
                                        create_time_format(self.model.granularity),
                                    ),
                                    "sunday",
                                ),
                                7,
                            )
                        ),
                        "yyyy-MM-dd HH:mm:ss",
                    ).alias("time_group"),
                ]
            )
        else:
            dataset_with_group = self.current.select(
                [
                    self.model.outputs.prediction.name,
                    self.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_format(
                                self.model.timestamp.name,
                                create_time_format(self.model.granularity),
                            )
                        ),
                        "yyyy-MM-dd HH:mm:ss",
                    ).alias("time_group"),
                ]
            )

        list_of_time_group = (
            dataset_with_group.select("time_group")
            .distinct()
            .orderBy(f.col("time_group").asc())
            .rdd.flatMap(lambda x: x)
            .collect()
        )
        array_of_groups = [
            dataset_with_group.where(f.col("time_group") == x)
            for x in list_of_time_group
        ]

        return {
            label: [
                {
                    "timestamp": group,
                    "value": self.__evaluate_multi_class_classification(
                        group_dataset, name
                    ),
                }
                for group, group_dataset in zip(list_of_time_group, array_of_groups)
            ]
            for name, label in self.model_quality_multiclass_classificator.items()
        }

    def calculate_binary_class_model_quality_group_by_timestamp(self):
        def create_time_format(granularity: Granularity):
            match granularity:
                case Granularity.HOUR:
                    return "yyyy-MM-dd HH"
                case Granularity.DAY:
                    return "yyyy-MM-dd"
                case Granularity.WEEK:
                    return "yyyy-MM-dd"
                case Granularity.MONTH:
                    return "yyyy-MM"

        if self.model.granularity == Granularity.WEEK:
            dataset_with_group = self.current.select(
                [
                    self.model.outputs.prediction_proba.name,
                    self.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_sub(
                                f.next_day(
                                    f.date_format(
                                        self.model.timestamp.name,
                                        create_time_format(self.model.granularity),
                                    ),
                                    "sunday",
                                ),
                                7,
                            )
                        ),
                        "yyyy-MM-dd HH:mm:ss",
                    ).alias("time_group"),
                ]
            )
        else:
            dataset_with_group = self.current.select(
                [
                    self.model.outputs.prediction_proba.name,
                    self.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_format(
                                self.model.timestamp.name,
                                create_time_format(self.model.granularity),
                            )
                        ),
                        "yyyy-MM-dd HH:mm:ss",
                    ).alias("time_group"),
                ]
            )

        list_of_time_group = (
            dataset_with_group.select("time_group")
            .distinct()
            .orderBy(f.col("time_group").asc())
            .rdd.flatMap(lambda x: x)
            .collect()
        )
        array_of_groups = [
            dataset_with_group.where(f.col("time_group") == x)
            for x in list_of_time_group
        ]

        return {
            label: [
                {
                    "timestamp": group,
                    "value": self.__evaluate_binary_classification(group_dataset, name),
                }
                for group, group_dataset in zip(list_of_time_group, array_of_groups)
            ]
            for name, label in self.model_quality_binary_classificator.items()
        }

    def calculate_confusion_matrix(self) -> dict[str, float]:
        prediction_and_label = (
            self.current.select(
                [self.model.outputs.prediction.name, self.model.target.name]
            )
            .withColumn(self.model.target.name, f.col(self.model.target.name))
            .orderBy(self.model.target.name)
        )

        tp = prediction_and_label.filter(
            (col(self.model.outputs.prediction.name) == 1)
            & (col(self.model.target.name) == 1)
        ).count()
        tn = prediction_and_label.filter(
            (col(self.model.outputs.prediction.name) == 0)
            & (col(self.model.target.name) == 0)
        ).count()
        fp = prediction_and_label.filter(
            (col(self.model.outputs.prediction.name) == 1)
            & (col(self.model.target.name) == 0)
        ).count()
        fn = prediction_and_label.filter(
            (col(self.model.outputs.prediction.name) == 0)
            & (col(self.model.target.name) == 1)
        ).count()

        return {
            "true_positive_count": tp,
            "false_positive_count": fp,
            "true_negative_count": tn,
            "false_negative_count": fn,
        }

    # FIXME use pydantic struct like data quality
    def calculate_model_quality_with_group_by_timestamp(self):
        metrics = dict()
        metrics["global_metrics"] = self.__calc_mc_metrics()
        metrics["grouped_metrics"] = (
            self.calculate_multiclass_model_quality_group_by_timestamp()
        )
        metrics["global_metrics"].update(self.calculate_confusion_matrix())
        if self.model.outputs.prediction_proba is not None:
            metrics["global_metrics"].update(self.__calc_bc_metrics())
            binary_class_metrics = (
                self.calculate_binary_class_model_quality_group_by_timestamp()
            )
            metrics["grouped_metrics"].update(binary_class_metrics)
        return metrics

    def calculate_drift(self):
        drift_result = dict()
        drift_result["feature_metrics"] = []

        categorical_features = [
            categorical.name for categorical in self.model.get_categorical_features()
        ]
        chi2 = Chi2Test(
            spark_session=self.spark_session,
            reference_data=self.reference,
            current_data=self.current,
        )

        for column in categorical_features:
            feature_dict_to_append = {
                "feature_name": column,
                "drift_calc": {
                    "type": "CHI2",
                },
            }
            if self.reference_count > 5 and self.current_count > 5:
                result_tmp = chi2.test(column, column)
                feature_dict_to_append["drift_calc"]["value"] = float(
                    result_tmp["pValue"]
                )
                feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                    result_tmp["pValue"] <= 0.05
                )
            else:
                feature_dict_to_append["drift_calc"]["value"] = None
                feature_dict_to_append["drift_calc"]["has_drift"] = False
            drift_result["feature_metrics"].append(feature_dict_to_append)

        numerical_features = [
            numerical.name for numerical in self.model.get_numerical_features()
        ]
        ks = KolmogorovSmirnovTest(
            reference_data=self.reference,
            current_data=self.current,
            alpha=0.05,
            phi=0.004,
        )

        for column in numerical_features:
            feature_dict_to_append = {
                "feature_name": column,
                "drift_calc": {
                    "type": "KS",
                },
            }
            result_tmp = ks.test(column, column)
            feature_dict_to_append["drift_calc"]["value"] = float(
                result_tmp["ks_statistic"]
            )
            feature_dict_to_append["drift_calc"]["has_drift"] = bool(
                result_tmp["ks_statistic"] > result_tmp["critical_value"]
            )
            drift_result["feature_metrics"].append(feature_dict_to_append)

        return drift_result
