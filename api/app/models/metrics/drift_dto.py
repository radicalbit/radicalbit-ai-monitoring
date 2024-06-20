from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.exceptions import MetricsInternalError
from app.models.job_status import JobStatus
from app.models.model_dto import ModelType


class DriftAlgorithm(str, Enum):
    KS = 'KS'
    CHI2 = 'CHI2'


class FeatureDriftCalculation(BaseModel):
    type: DriftAlgorithm
    value: Optional[float] = None
    has_drift: bool

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class FeatureMetrics(BaseModel):
    feature_name: str
    drift_calc: FeatureDriftCalculation

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class BinaryClassDrift(BaseModel):
    feature_metrics: List[FeatureMetrics]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MultiClassDrift(BaseModel):
    pass


class RegressionDrift(BaseModel):
    pass


class DriftDTO(BaseModel):
    job_status: JobStatus
    drift: Optional[Union[BinaryClassDrift, MultiClassDrift, RegressionDrift]]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_dict(
        model_type: ModelType,
        job_status: JobStatus,
        drift_data: Optional[Dict],
    ):
        if not drift_data:
            return DriftDTO(
                job_status=job_status,
                drift=None,
            )
        match model_type:
            case ModelType.BINARY:
                binary_class_data_quality = BinaryClassDrift(**drift_data)
                return DriftDTO(
                    job_status=job_status,
                    drift=binary_class_data_quality,
                )
            case ModelType.MULTI_CLASS:
                multi_class_data_quality = MultiClassDrift(**drift_data)
                return DriftDTO(
                    job_status=job_status,
                    drift=multi_class_data_quality,
                )
            case ModelType.REGRESSION:
                regression_data_quality = RegressionDrift(**drift_data)
                return DriftDTO(
                    job_status=job_status,
                    drift=regression_data_quality,
                )
            case _:
                raise MetricsInternalError(f'Invalid model type {model_type}')
