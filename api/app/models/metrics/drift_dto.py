from typing import Annotated, Any, Dict, List, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.drift_algorithm_type import DriftAlgorithmType
from app.models.inferred_schema_dto import FieldType
from app.models.job_status import JobStatus


class FeatureDriftCalculation(BaseModel):
    type: DriftAlgorithmType
    value: float
    has_drift: bool
    limit: float

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


def validate_old_drift(value: Any) -> Any:
    if isinstance(value, dict):
        return [value]
    return value


class FeatureMetrics(BaseModel):
    feature_name: str
    field_type: FieldType
    drift_calc: Annotated[
        List[FeatureDriftCalculation], BeforeValidator(validate_old_drift)
    ]

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
