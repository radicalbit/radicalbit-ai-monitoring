from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional


class ModelQuality(BaseModel):
    pass


class BinaryClassificationModelQuality(ModelQuality):
    f1: float
    accuracy: float
    precision: float
    recall: float
    f_measure: float
    weighted_precision: float
    weighted_recall: float
    weighted_f_measure: float
    weighted_true_positive_rate: float
    weighted_false_positive_rate: float
    true_positive_rate: float
    false_positive_rate: float
    true_positive_count: int
    false_positive_count: int
    true_negative_count: int
    false_negative_count: int
    area_under_roc: Optional[float] = None
    area_under_pr: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class MultiClassModelQuality(ModelQuality):
    pass


class RegressionModelQuality(ModelQuality):
    pass
