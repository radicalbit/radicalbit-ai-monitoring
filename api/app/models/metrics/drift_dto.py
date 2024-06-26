from enum import Enum
from typing import Dict, List, Optional

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
    drift: Optional[BinaryClassDrift | MultiClassDrift | RegressionDrift]

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
    ) -> 'DriftDTO':
        """
        Create a DriftDTO from a dictionary of data.
        """
        if not drift_data:
            return DriftDTO(
                job_status=job_status,
                drift=None,
            )

        drift = DriftDTO._create_drift(
            model_type=model_type,
            drift_data=drift_data,
        )

        return DriftDTO(
            job_status=job_status,
            drift=drift,
        )

    @staticmethod
    def _create_drift(
        model_type: ModelType,
        drift_data: Dict,
    ) -> BinaryClassDrift | MultiClassDrift | RegressionDrift:
        """
        Create a specific drift instance based on the model type.
        """
        if model_type == ModelType.BINARY:
            return BinaryClassDrift(**drift_data)
        elif model_type == ModelType.MULTI_CLASS:
            return MultiClassDrift(**drift_data)
        elif model_type == ModelType.REGRESSION:
            return RegressionDrift(**drift_data)
        else:
            raise MetricsInternalError(f'Invalid model type {model_type}')
