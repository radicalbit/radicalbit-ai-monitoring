from typing import List

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from radicalbit_platform_sdk.models.drift_algorithm_type import DriftAlgorithmType
from radicalbit_platform_sdk.models.field_type import FieldType


class FeatureDriftCalculation(BaseModel):
    type: DriftAlgorithmType
    value: float
    has_drift: bool
    limit: float

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class FeatureDrift(BaseModel):
    feature_name: str
    field_type: FieldType
    drift_calc: List[FeatureDriftCalculation]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class Drift(BaseModel):
    feature_metrics: List[FeatureDrift]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
