from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ModelQuality(BaseModel):
    pass


class BinaryClassificationModelQuality(ModelQuality):
    f1: Optional[float] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f_measure: Optional[float] = None
    weighted_precision: Optional[float] = None
    weighted_recall: Optional[float] = None
    weighted_f_measure: Optional[float] = None
    weighted_true_positive_rate: Optional[float] = None
    weighted_false_positive_rate: Optional[float] = None
    true_positive_rate: Optional[float] = None
    false_positive_rate: Optional[float] = None
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
