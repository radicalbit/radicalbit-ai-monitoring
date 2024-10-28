from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


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

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
