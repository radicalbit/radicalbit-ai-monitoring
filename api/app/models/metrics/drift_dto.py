from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.job_status import JobStatus


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


class Drift(BaseModel):
    feature_metrics: List[FeatureMetrics]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class DriftDTO(BaseModel):
    job_status: JobStatus
    drift: Optional[Drift]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_dict(
        job_status: JobStatus,
        drift_data: Optional[Dict],
    ) -> 'DriftDTO':
        """Create a DriftDTO from a dictionary of data."""
        drift = DriftDTO._create_drift(drift_data=drift_data)

        return DriftDTO(
            job_status=job_status,
            drift=drift,
        )

    @staticmethod
    def _create_drift(
        drift_data: Optional[Dict],
    ) -> Optional[Drift]:
        """Create a specific drift instance from a dictionary of data."""
        if not drift_data:
            return None
        return Drift(**drift_data)
