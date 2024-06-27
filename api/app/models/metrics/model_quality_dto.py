from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.dataset_type import DatasetType
from app.models.exceptions import MetricsInternalError
from app.models.job_status import JobStatus
from app.models.model_dto import ModelType


class MetricsBase(BaseModel):
    f1: Optional[float] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f_measure: Optional[float] = None
    weighted_precision: Optional[float] = None
    weighted_recall: Optional[float] = None
    weighted_f_measure: Optional[float] = None
    weighted_true_positive_rate: Optional[float] = None
    weighted_false_positive_rate: Optional[float] = None
    true_positive_rate: Optional[float] = None
    false_positive_rate: Optional[float] = None
    area_under_roc: Optional[float] = None
    area_under_pr: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class BinaryClassModelQuality(MetricsBase):
    true_positive_count: int
    false_positive_count: int
    true_negative_count: int
    false_negative_count: int


class Distribution(BaseModel):
    timestamp: str
    value: Optional[float] = None


class GroupedMetricsBase(BaseModel):
    f1: List[Distribution]
    accuracy: List[Distribution]
    precision: List[Distribution]
    recall: List[Distribution]
    f_measure: List[Distribution]
    weighted_precision: List[Distribution]
    weighted_recall: List[Distribution]
    weighted_f_measure: List[Distribution]
    weighted_true_positive_rate: List[Distribution]
    weighted_false_positive_rate: List[Distribution]
    true_positive_rate: List[Distribution]
    false_positive_rate: List[Distribution]
    area_under_roc: Optional[List[Distribution]] = None
    area_under_pr: Optional[List[Distribution]] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class CurrentBinaryClassModelQuality(BaseModel):
    global_metrics: BinaryClassModelQuality
    grouped_metrics: GroupedMetricsBase

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class ClassMetrics(BaseModel):
    class_name: str
    metrics: MetricsBase

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class MultiClassModelQuality(BaseModel):
    class_metrics: List[ClassMetrics]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class CurrentMultiClassModelQuality(BaseModel):
    pass


class RegressionModelQuality(BaseModel):
    pass


class ModelQualityDTO(BaseModel):
    job_status: JobStatus
    model_quality: Optional[
        BinaryClassModelQuality
        | CurrentBinaryClassModelQuality
        | MultiClassModelQuality
        | CurrentMultiClassModelQuality
        | RegressionModelQuality
    ]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_dict(
        dataset_type: DatasetType,
        model_type: ModelType,
        job_status: JobStatus,
        model_quality_data: Optional[Dict],
    ) -> 'ModelQualityDTO':
        """Create a ModelQualityDTO from a dictionary of data."""
        if not model_quality_data:
            return ModelQualityDTO(
                job_status=job_status,
                model_quality=None,
            )

        model_quality = ModelQualityDTO._create_model_quality(
            model_type=model_type,
            dataset_type=dataset_type,
            model_quality_data=model_quality_data,
        )

        return ModelQualityDTO(
            job_status=job_status,
            model_quality=model_quality,
        )

    @staticmethod
    def _create_model_quality(
        model_type: ModelType,
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> (
        BinaryClassModelQuality
        | CurrentBinaryClassModelQuality
        | MultiClassModelQuality
        | RegressionModelQuality
    ):
        """Create a specific model quality instance based on model type and dataset type."""
        if model_type == ModelType.BINARY:
            return ModelQualityDTO._create_binary_model_quality(
                dataset_type=dataset_type,
                model_quality_data=model_quality_data,
            )
        if model_type == ModelType.MULTI_CLASS:
            return ModelQualityDTO._create_multiclass_model_quality(
                dataset_type=dataset_type,
                model_quality_data=model_quality_data,
            )
        if model_type == ModelType.REGRESSION:
            return RegressionModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid model type {model_type}')

    @staticmethod
    def _create_binary_model_quality(
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> BinaryClassModelQuality | CurrentBinaryClassModelQuality:
        """Create a binary model quality instance based on dataset type."""
        if dataset_type == DatasetType.REFERENCE:
            return BinaryClassModelQuality(**model_quality_data)
        if dataset_type == DatasetType.CURRENT:
            return CurrentBinaryClassModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid dataset type {dataset_type}')

    @staticmethod
    def _create_multiclass_model_quality(
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> MultiClassModelQuality | CurrentMultiClassModelQuality:
        """Create a multiclass model quality instance based on dataset type."""
        if dataset_type == DatasetType.REFERENCE:
            return MultiClassModelQuality(**model_quality_data)
        if dataset_type == DatasetType.CURRENT:
            return CurrentMultiClassModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid dataset type {dataset_type}')
