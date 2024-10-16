from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.job_status import JobStatus


class DetailPercentage(BaseModel):
    feature_name: str
    score: float


class MetricPercentage(BaseModel):
    value: float
    details: List[Optional[DetailPercentage]] = None


class Percentages(BaseModel):
    data_quality: MetricPercentage
    model_quality: MetricPercentage
    drift: MetricPercentage

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class PercentagesDTO(BaseModel):
    job_status: JobStatus
    percentages: Optional[Percentages]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_dict(
        job_status: JobStatus,
        percentages_data: Optional[Dict],
    ) -> 'PercentagesDTO':
        """Create a PercentagesDTO from a dictionary of data."""
        percentages = PercentagesDTO._create_percentages(
            percentages_data=percentages_data
        )

        return percentages_data(
            job_status=job_status,
            percentages=percentages,
        )

    @staticmethod
    def _create_percentages(
        percentages_data: Optional[Dict],
    ) -> Optional[Percentages]:
        """Create a specific percentages instance from a dictionary of data."""
        if not percentages_data:
            return None
        return Percentages(**percentages_data)
