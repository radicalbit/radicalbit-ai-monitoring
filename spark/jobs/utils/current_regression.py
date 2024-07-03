from typing import List, Optional

from pyspark.sql import SparkSession

from metrics.data_quality_calculator import DataQualityCalculator
from models.current_dataset import CurrentDataset
from models.data_quality import (
    CategoricalFeatureMetrics,
    NumericalFeatureMetrics,
    NumericalTargetMetrics,
    RegressionDataQuality,
)
from models.reference_dataset import ReferenceDataset


class CurrentMetricsRegressionService:
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

    def calculate_target_metrics(self) -> NumericalTargetMetrics:
        return DataQualityCalculator.regression_target_metrics(
            target_column=self.current.model.target.name,
            dataframe=self.current.current,
            dataframe_count=self.current.current_count,
        )

    def calculate_current_target_metrics(self) -> NumericalTargetMetrics:
        return DataQualityCalculator.regression_target_metrics_current(
            target_column=self.current.model.target.name,
            curr_df=self.current.current,
            curr_count=self.current.current_count,
            ref_df=self.reference.reference,
            spark_session=self.spark_session,
        )

    def calculate_data_quality(
        self, is_current: Optional[bool] = False
    ) -> RegressionDataQuality:
        feature_metrics = []
        if self.reference.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.reference.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        target_metrics = (
            self.calculate_target_metrics()
            if not is_current
            else self.calculate_current_target_metrics()
        )
        return RegressionDataQuality(
            n_observations=self.current.current_count,
            target_metrics=target_metrics,
            feature_metrics=feature_metrics,
        )
