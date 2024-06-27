from typing import List

from metrics.data_quality_calculator import DataQualityCalculator
from models.reference_dataset import ReferenceDataset
from models.data_quality import (
    NumericalFeatureMetrics,
    CategoricalFeatureMetrics,
    ClassMetrics,
    MultiClassDataQuality,
)


class ReferenceMetricsMulticlassService:
    def __init__(self, reference: ReferenceDataset):
        self.reference = reference
        index_label_map, indexed_reference = reference.get_string_indexed_dataframe()
        self.index_label_map = index_label_map
        self.indexed_reference = indexed_reference

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

    def calculate_class_metrics(self) -> List[ClassMetrics]:
        return DataQualityCalculator.class_metrics(
            class_column=self.reference.model.target.name,
            dataframe=self.reference.reference,
            dataframe_count=self.reference.reference_count,
        )

    def calculate_data_quality(self) -> MultiClassDataQuality:
        feature_metrics = []
        if self.reference.model.get_numerical_features():
            feature_metrics.extend(self.calculate_data_quality_numerical())
        if self.reference.model.get_categorical_features():
            feature_metrics.extend(self.calculate_data_quality_categorical())
        return MultiClassDataQuality(
            n_observations=self.reference.reference_count,
            class_metrics=self.calculate_class_metrics(),
            feature_metrics=feature_metrics,
        )
