from models.regression_model_quality import ModelQualityRegression
from models.reference_dataset import ReferenceDataset
from metrics.model_quality_regression_calculator import ModelQualityRegressionCalculator


class ReferenceMetricsRegressionService:
    def __init__(self, reference: ReferenceDataset):
        self.reference = reference

    def calculate_model_quality(self) -> ModelQualityRegression:
        return ModelQualityRegressionCalculator.numerical_metrics(
            model=self.reference.model,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
        )
