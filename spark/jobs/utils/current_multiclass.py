from typing import Dict, List

from metrics.data_quality_calculator import DataQualityCalculator
from metrics.drift_calculator import DriftCalculator
from models.current_dataset import CurrentDataset
from models.data_quality import (
    CategoricalFeatureMetrics,
    ClassMetrics,
    MultiClassDataQuality,
    NumericalFeatureMetrics,
)
from models.reference_dataset import ReferenceDataset
from pandas import DataFrame
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from utils.misc import create_time_format
from utils.models import Granularity


class CurrentMetricsMulticlassService:
    def __init__(
        self,
        spark_session: SparkSession,
        current: CurrentDataset,
        reference: ReferenceDataset,
        prefix_id: str,
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

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        return DataQualityCalculator.calculate_combined_data_quality_numerical(
            model=self.current.model,
            current_dataframe=self.current.current,
            current_count=self.current.current_count,
            reference_dataframe=self.reference.reference,
            spark_session=self.spark_session,
            prefix_id=self.prefix_id,
        )

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        return DataQualityCalculator.categorical_metrics(
            model=self.current.model,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
            prefix_id=self.prefix_id,
        )

    def calculate_class_metrics(self, column) -> List[ClassMetrics]:
        return DataQualityCalculator.class_metrics(
            class_column=column,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
            prefix_id=self.prefix_id,
        )

    def calculate_multiclass_model_quality_group_by_timestamp(self):
        if self.current.model.granularity == Granularity.WEEK:
            dataset_with_group = self.indexed_current.select(
                [
                    f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx',
                    f'{self.prefix_id}_{self.current.model.target.name}-idx',
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
                                    'sunday',
                                ),
                                7,
                            )
                        ),
                        'yyyy-MM-dd HH:mm:ss',
                    ).alias('time_group'),
                ]
            )
        else:
            dataset_with_group = self.indexed_current.select(
                [
                    f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx',
                    f'{self.prefix_id}_{self.current.model.target.name}-idx',
                    self.current.model.outputs.prediction.name,
                    self.current.model.target.name,
                    F.date_format(
                        F.to_timestamp(
                            F.date_format(
                                self.current.model.timestamp.name,
                                create_time_format(self.current.model.granularity),
                            )
                        ),
                        'yyyy-MM-dd HH:mm:ss',
                    ).alias('time_group'),
                ]
            )

        # Cache for reuse
        dataset_with_group.cache()

        list_of_time_group = (
            dataset_with_group.select('time_group')
            .distinct()
            .orderBy(F.col('time_group').asc())
            .rdd.flatMap(lambda x: x)
            .collect()
        )

        pred_col = f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx'
        label_col = f'{self.prefix_id}_{self.current.model.target.name}-idx'

        # Batch compute all metrics using SQL operations instead of 2500 evaluator calls
        # Compute global metrics for all classes at once
        global_metrics_by_class = self.__batch_compute_metrics_for_all_classes(
            self.indexed_current, pred_col, label_col
        )

        # Compute time-grouped metrics for all classes and time groups at once
        grouped_metrics_data = self.__batch_compute_grouped_metrics(
            dataset_with_group, pred_col, label_col, list_of_time_group
        )

        # Build result structure matching original output format exactly
        result = [
            {
                'class_name': label,
                'metrics': global_metrics_by_class[index],
                'grouped_metrics': {
                    metric_label: [
                        {
                            'timestamp': group,
                            'value': grouped_metrics_data.get(
                                (group, index, metric_label), float('nan')
                            ),
                        }
                        for group in list_of_time_group
                    ]
                    for metric_label in self.model_quality_multiclass_classificator_by_label.values()
                },
            }
            for index, label in self.index_label_map.items()
        ]

        dataset_with_group.unpersist()

        return result

    def __batch_compute_metrics_for_all_classes(self, dataset, pred_col, label_col):
        """Batch compute all metrics for all classes using single aggregation"""
        from pyspark.sql.functions import col, sum as sql_sum, when
        
        # Single aggregation to compute ALL confusion matrix values at once
        class_indices = [float(idx) for idx in self.index_label_map.keys()]
        
        # Build aggregation expressions for all classes
        agg_exprs = []
        for class_idx in class_indices:
            agg_exprs.extend([
                sql_sum(when((col(pred_col) == class_idx) & (col(label_col) == class_idx), 1).otherwise(0)).alias(f'tp_{int(class_idx)}'),
                sql_sum(when((col(pred_col) == class_idx) & (col(label_col) != class_idx), 1).otherwise(0)).alias(f'fp_{int(class_idx)}'),
                sql_sum(when((col(pred_col) != class_idx) & (col(label_col) == class_idx), 1).otherwise(0)).alias(f'fn_{int(class_idx)}'),
                sql_sum(when((col(pred_col) != class_idx) & (col(label_col) != class_idx), 1).otherwise(0)).alias(f'tn_{int(class_idx)}'),
            ])
        
        # Execute single aggregation for ALL classes
        confusion_data = dataset.agg(*agg_exprs).collect()[0].asDict()
        
        # Compute metrics from collected confusion matrix
        metrics_by_class = {}
        for class_idx_str in self.index_label_map.keys():
            class_idx_int = int(float(class_idx_str))
            
            tp = confusion_data[f'tp_{class_idx_int}'] or 0
            fp = confusion_data[f'fp_{class_idx_int}'] or 0
            fn = confusion_data[f'fn_{class_idx_int}'] or 0
            tn = confusion_data[f'tn_{class_idx_int}'] or 0
            
            precision = float(tp) / (tp + fp) if (tp + fp) > 0 else float('nan')
            recall = float(tp) / (tp + fn) if (tp + fn) > 0 else float('nan')
            fpr = float(fp) / (fp + tn) if (fp + tn) > 0 else float('nan')
            f_measure = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            
            metrics_by_class[class_idx_str] = {
                'true_positive_rate': recall,
                'false_positive_rate': fpr,
                'precision': precision,
                'recall': recall,
                'f_measure': f_measure,
            }
        
        return metrics_by_class
    
    def __batch_compute_grouped_metrics(self, dataset, pred_col, label_col, time_groups):
        """Batch compute metrics for all time groups and classes using single aggregation"""
        from pyspark.sql.functions import col, sum as sql_sum, when
        
        class_indices = [float(idx) for idx in self.index_label_map.keys()]
        
        # Build aggregation expressions for all classes
        agg_exprs = []
        for class_idx in class_indices:
            agg_exprs.extend([
                sql_sum(when((col(pred_col) == class_idx) & (col(label_col) == class_idx), 1).otherwise(0)).alias(f'tp_{int(class_idx)}'),
                sql_sum(when((col(pred_col) == class_idx) & (col(label_col) != class_idx), 1).otherwise(0)).alias(f'fp_{int(class_idx)}'),
                sql_sum(when((col(pred_col) != class_idx) & (col(label_col) == class_idx), 1).otherwise(0)).alias(f'fn_{int(class_idx)}'),
                sql_sum(when((col(pred_col) != class_idx) & (col(label_col) != class_idx), 1).otherwise(0)).alias(f'tn_{int(class_idx)}'),
            ])
        
        # Single aggregation grouped by time_group for ALL classes and time groups at once!
        confusion_by_time = (
            dataset
            .groupBy('time_group')
            .agg(*agg_exprs)
            .collect()
        )
        
        # Convert to lookup dictionary
        grouped_metrics = {}
        for row in confusion_by_time:
            time_group = row['time_group']
            
            for class_idx_str in self.index_label_map.keys():
                class_idx_int = int(float(class_idx_str))
                
                tp = row[f'tp_{class_idx_int}'] or 0
                fp = row[f'fp_{class_idx_int}'] or 0
                fn = row[f'fn_{class_idx_int}'] or 0
                tn = row[f'tn_{class_idx_int}'] or 0

                print(tp)
                print(fp)
                print(fn)
                print(tn)


                precision = float(tp) / (tp + fp) if (tp + fp) > 0 else float('nan')
                recall = float(tp) / (tp + fn) if (tp + fn) > 0 else float('nan')
                fpr = float(fp) / (fp + tn) if (fp + tn) > 0 else float('nan')
                print(precision)
                print(recall)
                f_measure = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
                
                grouped_metrics[(time_group, class_idx_str, 'true_positive_rate')] = recall
                grouped_metrics[(time_group, class_idx_str, 'false_positive_rate')] = fpr
                grouped_metrics[(time_group, class_idx_str, 'precision')] = precision
                grouped_metrics[(time_group, class_idx_str, 'recall')] = recall
                grouped_metrics[(time_group, class_idx_str, 'f_measure')] = f_measure
        
        return grouped_metrics

    def __evaluate_multi_class_classification(
        self, dataset: DataFrame, metric_name: str, class_index: float
    ) -> float:
        try:
            return MulticlassClassificationEvaluator(
                metricName=metric_name,
                predictionCol=f'{self.prefix_id}_{self.current.model.outputs.prediction.name}-idx',
                labelCol=f'{self.prefix_id}_{self.current.model.target.name}-idx',
                metricLabel=class_index,
            ).evaluate(dataset)
        except Exception:
            return float('nan')

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
                f'{self.prefix_id}_{self.reference.model.outputs.prediction.name}-idx',
                f'{self.prefix_id}_{self.reference.model.target.name}-idx',
            ]
        ).rdd
        multiclass_metrics_calculator = MulticlassMetrics(prediction_and_labels)
        return multiclass_metrics_calculator.confusionMatrix().toArray().tolist()

    def calculate_model_quality(self) -> Dict:
        metrics_by_label = self.calculate_multiclass_model_quality_group_by_timestamp()
        global_metrics = self.__calc_multiclass_global_metrics()
        global_metrics['confusion_matrix'] = self.__calc_confusion_matrix()
        return {
            'classes': list(self.index_label_map.values()),
            'class_metrics': metrics_by_label,
            'global_metrics': global_metrics,
        }

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
            prefix_id=self.prefix_id,
        )
