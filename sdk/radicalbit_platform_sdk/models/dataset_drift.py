from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DriftAlgorithm(str, Enum):
    KS = "KS"
    CHI2 = "CHI2"


class FeatureDriftCalculation(BaseModel):
    type: DriftAlgorithm
    value: Optional[float] = None
    has_drift: bool

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class FeatureDrift(BaseModel):
    feature_name: str
    drift_calc: FeatureDriftCalculation

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class Drift(BaseModel):
    pass


class BinaryClassDrift(Drift):
    feature_metrics: List[FeatureDrift]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MultiClassDrift(Drift):
    pass


class RegressionDrift(BaseModel):
    pass
