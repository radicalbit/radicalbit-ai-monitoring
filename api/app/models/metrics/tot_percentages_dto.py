from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class TotPercentagesDTO(BaseModel):
    data_quality: float
    model_quality: float
    drift: float

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def from_dict(
        tot_percentages_data: Optional[Dict],
    ) -> 'TotPercentagesDTO':
        """Create a PercentagesDTO from a dictionary of data."""

        return TotPercentagesDTO.model_validate(tot_percentages_data)
