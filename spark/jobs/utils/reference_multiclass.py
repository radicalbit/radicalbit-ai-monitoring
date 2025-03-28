from typing import Dict, List

from metrics.data_quality_calculator import DataQualityCalculator
from models.data_quality import (
    CategoricalFeatureMetrics,
    ClassMetrics,
    MultiClassDataQuality,
    NumericalFeatureMetrics,
)
from models.reference_dataset import ReferenceDataset
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql import DataFrame
import pyspark.sql.functions as f

# from utils.misc import rbit_prefix


class ReferenceMetricsMulticlassService:
    def __init__(self, reference: ReferenceDataset, prefix_id: str):
        self.reference = reference
        index_label_map, indexed_reference = reference.get_string_indexed_dataframe()
        self.index_label_map = index_label_map
        self.indexed_reference = indexed_reference
        self.model_quality_multiclass_classificator_global = {
            'f1': 'f1',
            'accuracy': 'accuracy',
            'weightedPrecision': 'weighted_precision',
            'weightedRecall': 'weighted_recall',
            'weightedTruePositiveRate': 'weighted_true_positive_rate',
            'weightedFalsePositiveRate': 'weighted_false_positive_rate',
            'weightedFMeasure': 'weighted_f_measure',
        }
        self.model_quality_multiclass_classificator_by_label = {
            'truePositiveRateByLabel': 'true_positive_rate',
            'falsePositiveRateByLabel': 'false_positive_rate',
            'precisionByLabel': 'precision',
            'recallByLabel': 'recall',
            'fMeasureByLabel': 'f_measure',
        }
        self.prefix_id = prefix_id

    def __evaluate_multi_class_classification(
        self, dataset: DataFrame, metric_name: str, class_index: float
    ) -> float:
        try:
            return MulticlassClassificationEvaluator(
                metricName=metric_name,
                predictionCol=f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx',
                labelCol=f'{self.prefix_id}_{self.reference.model.target.name}-idx',
                metricLabel=class_index,
            ).evaluate(dataset)
        except Exception:
            return float('nan')

    # FIXME use pydantic struct like data quality
    def __calc_multiclass_by_label_metrics(self) -> List[Dict]:
        return [
            {
                'class_name': label,
                'metrics': {
                    metric_label: self.__evaluate_multi_class_classification(
                        self.indexed_reference.filter(
                            ~(
                                f.col(
                                    self.reference.model.outputs.prediction.name
                                ).isNull()
                                | f.isnan(
                                    f.col(self.reference.model.outputs.prediction.name)
                                )
                            )
                            & ~(
                                f.col(self.reference.model.target.name).isNull()
                                | f.isnan(f.col(self.reference.model.target.name))
                            )
                        ),
                        metric_name,
                        float(index),
                    )
                    for (
                        metric_name,
                        metric_label,
                    ) in self.model_quality_multiclass_classificator_by_label.items()
                },
            }
            for index, label in self.index_label_map.items()
        ]

    def __calc_multiclass_global_metrics(self) -> Dict:
        return {
            metric_label: self.__evaluate_multi_class_classification(
                self.indexed_reference, metric_name, 0.0
            )
            for (
                metric_name,
                metric_label,
            ) in self.model_quality_multiclass_classificator_global.items()
        }

    def __calc_confusion_matrix(self):
        prediction_and_labels = (
            self.indexed_reference.filter(
                ~(
                    f.col(self.reference.model.outputs.prediction.name).isNull()
                    | f.isnan(f.col(self.reference.model.outputs.prediction.name))
                )
                & ~(
                    f.col(self.reference.model.target.name).isNull()
                    | f.isnan(f.col(self.reference.model.target.name))
                )
            )
            .select(
                *[
                    f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx',
                    f'{self.prefix_id}_{self.reference.model.target.name}-idx',
                ]
            )
            .rdd
        )
        multiclass_metrics_calculator = MulticlassMetrics(prediction_and_labels)
        return multiclass_metrics_calculator.confusionMatrix().toArray().tolist()

    def calculate_model_quality(self) -> Dict:
        metrics_by_label = self.__calc_multiclass_by_label_metrics()
        global_metrics = self.__calc_multiclass_global_metrics()
        global_metrics['confusion_matrix'] = self.__calc_confusion_matrix()
        return {
            'classes': list(self.index_label_map.values()),
            'class_metrics': metrics_by_label,
            'global_metrics': global_metrics,
        }

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        return DataQualityCalculator.numerical_metrics(
            model=self.reference.model,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
        )

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        return DataQualityCalculator.categorical_metrics(
            model=self.reference.model,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
            prefix_id=self.prefix_id,
        )

    def calculate_class_metrics(self, column) -> List[ClassMetrics]:
        return DataQualityCalculator.class_metrics(
            class_column=column,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
            prefix_id=self.prefix_id,
        )

    def calculate_data_quality(self) -> MultiClassDataQuality:
        feature_metrics = []
        if self.reference.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.reference.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return MultiClassDataQuality(
            n_observations=self.reference.reference_count,
            class_metrics=self.calculate_class_metrics(
                self.reference.model.target.name
            ),
            class_metrics_prediction=self.calculate_class_metrics(
                self.reference.model.outputs.prediction.name
            ),
            feature_metrics=feature_metrics,
        )
