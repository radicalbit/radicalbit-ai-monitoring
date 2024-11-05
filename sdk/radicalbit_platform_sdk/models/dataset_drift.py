from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from radicalbit_platform_sdk.models.field_type import FieldType


class DriftAlgorithm(str, Enum):
    KS = 'KS'
    CHI2 = 'CHI2'
    PSI = 'PSI'


class FeatureDriftCalculation(BaseModel):
    type: DriftAlgorithm
    value: Optional[float] = None
    has_drift: bool

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class FeatureDrift(BaseModel):
    feature_name: str
    field_type: FieldType
    drift_calc: FeatureDriftCalculation

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class Drift(BaseModel):
    feature_metrics: List[FeatureDrift]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
