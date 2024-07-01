from typing import List

from pyspark.sql import DataFrame, SparkSession

from metrics.data_quality_calculator import DataQualityCalculator
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    MultiClassDataQuality,
)
from utils.models import ModelOut


class CurrentMetricsMulticlassService:
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
            model=self.model,
            dataframe=self.reference,
            dataframe_count=self.reference_count,
        )

    def calculate_class_metrics(self) -> List[ClassMetrics]:
        return DataQualityCalculator.class_metrics(
            class_column=self.model.target.name,
            dataframe=self.reference,
            dataframe_count=self.reference_count,
        )

    def calculate_data_quality(self) -> MultiClassDataQuality:
        feature_metrics = []
        if self.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return MultiClassDataQuality(
            n_observations=self.reference_count,
            class_metrics=self.calculate_class_metrics(),
            feature_metrics=feature_metrics,
        )
