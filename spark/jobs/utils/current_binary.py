from typing import List

from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator,
)
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as f

from metrics.data_quality_calculator import DataQualityCalculator
from metrics.drift_calculator import DriftCalculator
from models.current_dataset import CurrentDataset
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    BinaryClassDataQuality,
)
from models.reference_dataset import ReferenceDataset
from .misc import create_time_format
from .models import Granularity


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
        current: CurrentDataset,
        reference: ReferenceDataset,
    ):
        self.spark_session = spark_session
        self.current = current
        self.reference = reference

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        return DataQualityCalculator.calculate_combined_data_quality_numerical(
            model=self.current.model,
            current_dataframe=self.current.current,
            current_count=self.current.current_count,
            reference_dataframe=self.reference.reference,
            spark_session=self.spark_session,
        )

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        return DataQualityCalculator.categorical_metrics(
            model=self.current.model,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
        )

    def calculate_class_metrics(self) -> List[ClassMetrics]:
        metrics = DataQualityCalculator.class_metrics(
            class_column=self.current.model.target.name,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
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
        if self.current.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.current.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return BinaryClassDataQuality(
            n_observations=self.current.current_count,
            class_metrics=self.calculate_class_metrics(),
            feature_metrics=feature_metrics,
        )

    # FIXME use pydantic struct like data quality
    def __calc_bc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_binary_classification(self.current.current, name)
            for (name, label) in self.model_quality_binary_classificator.items()
        }

    # FIXME use pydantic struct like data quality
    def __calc_mc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_multi_class_classification(
                self.current.current.filter(
                    ~(
                        f.col(self.current.model.outputs.prediction.name).isNull()
                        | f.isnan(f.col(self.current.model.outputs.prediction.name))
                    )
                    & ~(
                        f.col(self.current.model.target.name).isNull()
                        | f.isnan(f.col(self.current.model.target.name))
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
                labelCol=self.current.model.target.name,
                rawPredictionCol=self.current.model.outputs.prediction_proba.name,
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
                predictionCol=self.current.model.outputs.prediction.name,
                labelCol=self.current.model.target.name,
                metricLabel=1,
            ).evaluate(dataset)
        except Exception:
            return float("nan")

    def calculate_multiclass_model_quality_group_by_timestamp(self):

        current_df_clean = self.current.current.filter(
            ~(
                f.col(self.current.model.outputs.prediction.name).isNull()
                | f.isnan(f.col(self.current.model.outputs.prediction.name))
            )
            & ~(
                f.col(self.current.model.target.name).isNull()
                | f.isnan(f.col(self.current.model.target.name))
            )
        )

        if self.current.model.granularity == Granularity.WEEK:
            dataset_with_group = current_df_clean.select(
                [
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_sub(
                                f.next_day(
                                    f.date_format(
                                        self.current.model.timestamp.name,
                                        create_time_format(
                                            self.current.model.granularity
                                        ),
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
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_format(
                                self.current.model.timestamp.name,
                                create_time_format(self.current.model.granularity),
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

        current_df_clean = self.current.filter(
            ~(
                f.col(self.current.model.outputs.prediction_proba.name).isNull()
                | f.isnan(f.col(self.current.model.outputs.prediction_proba.name))
            )
            & ~(
                f.col(self.current.model.target.name).isNull()
                | f.isnan(f.col(self.current.model.target.name))
            )
        )

        if self.current.model.granularity == Granularity.WEEK:
            dataset_with_group = current_df_clean.select(
                [
                    self.current.model.outputs.prediction_proba.name,
                    self.current.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_sub(
                                f.next_day(
                                    f.date_format(
                                        self.current.model.timestamp.name,
                                        create_time_format(
                                            self.current.model.granularity
                                        ),
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
                    self.current.model.outputs.prediction_proba.name,
                    self.current.model.target.name,
                    f.date_format(
                        f.to_timestamp(
                            f.date_format(
                                self.current.model.timestamp.name,
                                create_time_format(self.current.model.granularity),
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
            self.current.current.filter(
                ~(
                    f.col(self.current.model.outputs.prediction.name).isNull()
                    | f.isnan(f.col(self.current.model.outputs.prediction.name))
                )
                & ~(
                    f.col(self.current.model.target.name).isNull()
                    | f.isnan(f.col(self.current.model.target.name))
                )
            )
            .select([self.current.model.outputs.prediction.name, self.current.model.target.name])
            .withColumn(self.current.model.target.name, f.col(self.current.model.target.name))
            .orderBy(self.current.model.target.name)
        )

        tp = prediction_and_label.filter(
            (col(self.current.model.outputs.prediction.name) == 1)
            & (col(self.current.model.target.name) == 1)
        ).count()
        tn = prediction_and_label.filter(
            (col(self.current.model.outputs.prediction.name) == 0)
            & (col(self.current.model.target.name) == 0)
        ).count()
        fp = prediction_and_label.filter(
            (col(self.current.model.outputs.prediction.name) == 1)
            & (col(self.current.model.target.name) == 0)
        ).count()
        fn = prediction_and_label.filter(
            (col(self.current.model.outputs.prediction.name) == 0)
            & (col(self.current.model.target.name) == 1)
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
        if self.current.model.outputs.prediction_proba is not None:
            metrics["global_metrics"].update(self.__calc_bc_metrics())
            binary_class_metrics = (
                self.calculate_binary_class_model_quality_group_by_timestamp()
            )
            metrics["grouped_metrics"].update(binary_class_metrics)
        return metrics

    def calculate_drift(self):
        return DriftCalculator.calculate_drift(
            spark_session=self.spark_session,
            reference_dataset=self.reference,
            current_dataset=self.current,
        )
