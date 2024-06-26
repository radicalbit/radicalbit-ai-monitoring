import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.job_status import JobStatus


class Statistics(BaseModel):
    n_variables: int
    n_observations: int
    missing_cells: int
    missing_cells_perc: Optional[float]
    duplicate_rows: int
    duplicate_rows_perc: Optional[float]
    numeric: int
    categorical: int
    datetime: int

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class StatisticsDTO(BaseModel):
    job_status: JobStatus
    statistics: Optional[Statistics]
    date: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_dict(
        job_status: JobStatus, date: datetime, statistics_data: Optional[Dict]
    ) -> 'StatisticsDTO':
        """
        Create a StatisticsDTO from a dictionary of data.
        """
        statistics = StatisticsDTO._create_statistics(statistics_data)
        return StatisticsDTO(
            job_status=job_status,
            statistics=statistics,
            date=date.isoformat(),
        )

    @staticmethod
    def _create_statistics(
        statistics_data: Optional[Dict],
    ) -> Optional[Statistics]:
        """
        Create a Statistics instance from a dictionary of data.
        """
        if not statistics_data:
            return None
        return Statistics(**statistics_data)
