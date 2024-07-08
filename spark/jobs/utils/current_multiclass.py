from typing import List, Dict

from pandas import DataFrame
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from metrics.data_quality_calculator import DataQualityCalculator
from metrics.drift_calculator import DriftCalculator
from models.current_dataset import CurrentDataset
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    MultiClassDataQuality,
)
from models.reference_dataset import ReferenceDataset
from utils.misc import create_time_format
from utils.models import Granularity


class CurrentMetricsMulticlassService:
    def __init__(
        self,
        spark_session: SparkSession,
        current: CurrentDataset,
        reference: ReferenceDataset,
    ):
        self.spark_session = spark_session
        self.current = current
        self.reference = reference
        index_label_map, indexed_current = current.get_string_indexed_dataframe(
            self.reference
        )
        self.index_label_map = index_label_map
        self.indexed_current = indexed_current
        self.model_quality_multiclass_classificator_global = {
            "f1": "f1",
            "accuracy": "accuracy",
            "weightedPrecision": "weighted_precision",
            "weightedRecall": "weighted_recall",
            "weightedTruePositiveRate": "weighted_true_positive_rate",
            "weightedFalsePositiveRate": "weighted_false_positive_rate",
            "weightedFMeasure": "weighted_f_measure",
        }
        self.model_quality_multiclass_classificator_by_label = {
            "truePositiveRateByLabel": "true_positive_rate",
            "falsePositiveRateByLabel": "false_positive_rate",
            "precisionByLabel": "precision",
            "recallByLabel": "recall",
            "fMeasureByLabel": "f_measure",
        }

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

    def calculate_class_metrics(self, column) -> List[ClassMetrics]:
        return DataQualityCalculator.class_metrics(
            class_column=column,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
        )

    def calculate_multiclass_model_quality_group_by_timestamp(self):
        if self.current.model.granularity == Granularity.WEEK:
            dataset_with_group = self.indexed_current.select(
                [
                    f"{self.reference.model.outputs.prediction.name}-idx",
                    f"{self.current.model.target.name}-idx",
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    F.date_format(
                        F.to_timestamp(
                            F.date_sub(
                                F.next_day(
                                    F.date_format(
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
            dataset_with_group = self.indexed_current.select(
                [
                    f"{self.reference.model.outputs.prediction.name}-idx",
                    f"{self.current.model.target.name}-idx",
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    F.date_format(
                        F.to_timestamp(
                            F.date_format(
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
            .orderBy(F.col("time_group").asc())
            .rdd.flatMap(lambda x: x)
            .collect()
        )
        array_of_groups = [
            dataset_with_group.where(F.col("time_group") == x)
            for x in list_of_time_group
        ]

        return [
            {
                "class_name": label,
                "metrics": {
                    metric_label: self.__evaluate_multi_class_classification(
                        self.indexed_current, metric_name, float(index)
                    )
                    for (
                        metric_name,
                        metric_label,
                    ) in self.model_quality_multiclass_classificator_by_label.items()
                },
                "grouped_metrics": {
                    metric_label: [
                        {
                            "timestamp": group,
                            "value": self.__evaluate_multi_class_classification(
                                group_dataset, metric_name, float(index)
                            ),
                        }
                        for group, group_dataset in zip(
                            list_of_time_group, array_of_groups
                        )
                    ]
                    for metric_name, metric_label in self.model_quality_multiclass_classificator_by_label.items()
                },
            }
            for index, label in self.index_label_map.items()
        ]

    def __evaluate_multi_class_classification(
        self, dataset: DataFrame, metric_name: str, class_index: float
    ) -> float:
        try:
            return MulticlassClassificationEvaluator(
                metricName=metric_name,
                predictionCol=f"{self.current.model.outputs.prediction.name}-idx",
                labelCol=f"{self.current.model.target.name}-idx",
                metricLabel=class_index,
            ).evaluate(dataset)
        except Exception:
            return float("nan")

    def __calc_multiclass_global_metrics(self) -> Dict:
        return {
            metric_label: self.__evaluate_multi_class_classification(
                self.indexed_current, metric_name, 0.0
            )
            for (
                metric_name,
                metric_label,
            ) in self.model_quality_multiclass_classificator_global.items()
        }

    def __calc_confusion_matrix(self):
        prediction_and_labels = self.indexed_current.select(
            *[
                f"{self.reference.model.outputs.prediction.name}-idx",
                f"{self.reference.model.target.name}-idx",
            ]
        ).rdd
        multiclass_metrics_calculator = MulticlassMetrics(prediction_and_labels)
        return multiclass_metrics_calculator.confusionMatrix().toArray().tolist()

    def calculate_model_quality(self) -> Dict:
        metrics_by_label = self.calculate_multiclass_model_quality_group_by_timestamp()
        global_metrics = self.__calc_multiclass_global_metrics()
        global_metrics["confusion_matrix"] = self.__calc_confusion_matrix()
        metrics = {
            "classes": list(self.index_label_map.values()),
            "class_metrics": metrics_by_label,
            "global_metrics": global_metrics,
        }

        return metrics

    def calculate_data_quality(self) -> MultiClassDataQuality:
        feature_metrics = []
        if self.current.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.current.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return MultiClassDataQuality(
            n_observations=self.current.current_count,
            class_metrics=self.calculate_class_metrics(self.current.model.target.name),
            class_metrics_prediction=self.calculate_class_metrics(
                self.current.model.outputs.prediction.name
            ),
            feature_metrics=feature_metrics,
        )

    def calculate_drift(self):
        return DriftCalculator.calculate_drift(
            spark_session=self.spark_session,
            reference_dataset=self.reference,
            current_dataset=self.current,
        )
