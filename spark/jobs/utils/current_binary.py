from typing import List

from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator,
)
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as f

from metrics.data_quality_calculator import DataQualityCalculator
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    BinaryClassDataQuality,
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
        return DataQualityCalculator.calculate_combined_data_quality_numerical(
            model=self.model,
            current_dataframe=self.current,
            current_count=self.current_count,
            reference_dataframe=self.reference,
            spark_session=self.spark_session,
        )

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

    # FIXME use pydantic struct like data quality
    def __calc_bc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_binary_classification(self.current, name)
            for (name, label) in self.model_quality_binary_classificator.items()
        }

    # FIXME use pydantic struct like data quality
    def __calc_mc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_multi_class_classification(
                self.current.filter(
                    ~(
                        f.col(self.model.outputs.prediction.name).isNull()
                        | f.isnan(f.col(self.model.outputs.prediction.name))
                    )
                    & ~(
                        f.col(self.model.target.name).isNull()
                        | f.isnan(f.col(self.model.target.name))
                    )
                ),
                name,
            )
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

        current_df_clean = self.current.filter(
            ~(
                f.col(self.model.outputs.prediction.name).isNull()
                | f.isnan(f.col(self.model.outputs.prediction.name))
            )
            & ~(
                f.col(self.model.target.name).isNull()
                | f.isnan(f.col(self.model.target.name))
            )
        )

        if self.model.granularity == Granularity.WEEK:
            dataset_with_group = current_df_clean.select(
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
            dataset_with_group = current_df_clean.select(
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

        current_df_clean = self.current.filter(
            ~(
                f.col(self.model.outputs.prediction_proba.name).isNull()
                | f.isnan(f.col(self.model.outputs.prediction_proba.name))
            )
            & ~(
                f.col(self.model.target.name).isNull()
                | f.isnan(f.col(self.model.target.name))
            )
        )

        if self.model.granularity == Granularity.WEEK:
            dataset_with_group = current_df_clean.select(
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
            dataset_with_group = current_df_clean.select(
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
            self.current.filter(
                ~(
                    f.col(self.model.outputs.prediction.name).isNull()
                    | f.isnan(f.col(self.model.outputs.prediction.name))
                )
                & ~(
                    f.col(self.model.target.name).isNull()
                    | f.isnan(f.col(self.model.target.name))
                )
            )
            .select([self.model.outputs.prediction.name, self.model.target.name])
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
