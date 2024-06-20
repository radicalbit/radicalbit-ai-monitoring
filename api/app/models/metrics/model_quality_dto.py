from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.dataset_type import DatasetType
from app.models.exceptions import MetricsInternalError
from app.models.job_status import JobStatus
from app.models.model_dto import ModelType


class BinaryClassModelQuality(BaseModel):
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
    true_positive_count: int
    false_positive_count: int
    true_negative_count: int
    false_negative_count: int
    area_under_roc: Optional[float] = None
    area_under_pr: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class Distribution(BaseModel):
    timestamp: str
    value: Optional[float] = None


class GroupedBinaryClassModelQuality(BaseModel):
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
    grouped_metrics: GroupedBinaryClassModelQuality

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class MultiClassModelQuality(BaseModel):
    pass


class RegressionModelQuality(BaseModel):
    pass


class ModelQualityDTO(BaseModel):
    job_status: JobStatus
    model_quality: Optional[
        Union[
            BinaryClassModelQuality,
            CurrentBinaryClassModelQuality,
            MultiClassModelQuality,
            RegressionModelQuality,
        ]
    ]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_dict(
        dataset_type: DatasetType = DatasetType.REFERENCE,
        model_type: ModelType = ModelType.BINARY,
        job_status: JobStatus = JobStatus.SUCCEEDED,
        model_quality_data: Optional[Dict] = None,
    ):
        if not model_quality_data:
            return ModelQualityDTO(
                job_status=job_status,
                model_quality=None,
            )
        match model_type:
            case ModelType.BINARY:
                match dataset_type:
                    case DatasetType.REFERENCE:
                        binary_class_model_quality = BinaryClassModelQuality(
                            **model_quality_data
                        )
                        return ModelQualityDTO(
                            job_status=job_status,
                            model_quality=binary_class_model_quality,
                        )
                    case DatasetType.CURRENT:
                        current_binary_class_model_quality = (
                            CurrentBinaryClassModelQuality(**model_quality_data)
                        )
                        return ModelQualityDTO(
                            job_status=job_status,
                            model_quality=current_binary_class_model_quality,
                        )
            case ModelType.MULTI_CLASS:
                multi_class_model_quality = MultiClassModelQuality(**model_quality_data)
                return ModelQualityDTO(
                    job_status=job_status,
                    model_quality=multi_class_model_quality,
                )
            case ModelType.REGRESSION:
                regression_model_quality = RegressionModelQuality(**model_quality_data)
                return ModelQualityDTO(
                    job_status=job_status,
                    model_quality=regression_model_quality,
                )
            case _:
                raise MetricsInternalError(f'Invalid model type {model_type}')
