from typing import List

from pyspark.sql import DataFrame
from pyspark.ml.evaluation import (
    BinaryClassificationEvaluator,
    MulticlassClassificationEvaluator,
)
from pyspark.sql.functions import col
import pyspark.sql.functions as f

from metrics.data_quality_calculator import DataQualityCalculator
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    BinaryClassDataQuality,
)
from .models import ModelOut


class ReferenceMetricsService:
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

    def __init__(self, reference: DataFrame, model: ModelOut):
        self.model = model
        self.reference = reference
        self.reference_count = self.reference.count()

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

    # FIXME use pydantic struct like data quality
    def __calc_bc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_binary_classification(self.reference, name)
            for (name, label) in self.model_quality_binary_classificator.items()
        }

    # FIXME use pydantic struct like data quality
    def __calc_mc_metrics(self) -> dict[str, float]:
        return {
            label: self.__evaluate_multi_class_classification(self.reference, name)
            for (name, label) in self.model_quality_multiclass_classificator.items()
        }

    # FIXME use pydantic struct like data quality
    def calculate_model_quality(self) -> dict[str, float]:
        metrics = self.__calc_mc_metrics()
        metrics.update(self.calculate_confusion_matrix())
        if self.model.outputs.prediction_proba is not None:
            metrics.update(self.__calc_bc_metrics())

        return metrics

    # FIXME use pydantic struct like data quality
    def calculate_confusion_matrix(self) -> dict[str, float]:
        prediction_and_label = (
            self.reference.select(
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

    def calculate_data_quality_numerical(self) -> List[NumericalFeatureMetrics]:
        return DataQualityCalculator.numerical_metrics(
            model=self.model,
            dataframe=self.reference,
            dataframe_count=self.reference_count,
        )

    def calculate_data_quality_categorical(self) -> List[CategoricalFeatureMetrics]:
        return DataQualityCalculator.categorical_metrics(
            model=self.model,
            dataframe=self.reference,
            dataframe_count=self.reference_count,
        )

    def calculate_class_metrics(self) -> List[ClassMetrics]:
        metrics = DataQualityCalculator.class_metrics(
            class_column=self.model.target.name,
            dataframe=self.reference,
            dataframe_count=self.reference_count,
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
            n_observations=self.reference_count,
            class_metrics=self.calculate_class_metrics(),
            feature_metrics=feature_metrics,
        )
