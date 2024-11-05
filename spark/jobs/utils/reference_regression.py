from typing import List
from models.regression_model_quality import ModelQualityRegression
from models.reference_dataset import ReferenceDataset
from metrics.model_quality_regression_calculator import ModelQualityRegressionCalculator
from models.data_quality import (
    CategoricalFeatureMetrics,
    NumericalFeatureMetrics,
    NumericalTargetMetrics,
    RegressionDataQuality,
)
from metrics.data_quality_calculator import DataQualityCalculator


class ReferenceMetricsRegressionService:
    def __init__(self, reference: ReferenceDataset):
        self.reference = reference

    def calculate_model_quality(self) -> ModelQualityRegression:
        metrics = ModelQualityRegressionCalculator.numerical_metrics(
            model=self.reference.model,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
        ).dict()

        metrics["residuals"] = ModelQualityRegressionCalculator.residual_metrics(
            model=self.reference.model,
            dataframe=self.reference.reference,
        )

        return metrics

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
        )

    def calculate_target_metrics(self) -> NumericalTargetMetrics:
        return DataQualityCalculator.regression_target_metrics(
            target_column=self.reference.model.target.name,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
        )

    def calculate_data_quality(self) -> RegressionDataQuality:
        feature_metrics = []
        if self.reference.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.reference.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        target_metrics = self.calculate_target_metrics()
        return RegressionDataQuality(
            n_observations=self.reference.reference_count,
            target_metrics=target_metrics,
            feature_metrics=feature_metrics,
        )
