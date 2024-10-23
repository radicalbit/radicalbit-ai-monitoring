from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AnomalyType(str, Enum):
    data_quality = 'data_quality'
    model_quality = 'model_quality'
    drift = 'drift'


class AlertDTO(BaseModel):
    model_uuid: UUID
    reference_uuid: Optional[UUID]
    current_uuid: Optional[UUID]
    anomaly_type: AnomalyType
    anomaly_features: List[str]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_dict(
        alert_data: Optional[Dict],
    ) -> 'AlertDTO':
        """Create a PercentagesDTO from a dictionary of data."""

        return AlertDTO.model_validate(alert_data)
