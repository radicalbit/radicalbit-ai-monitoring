from typing import List, Optional

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


class Distribution(BaseModel):
    timestamp: str
    value: Optional[float] = None


class GroupedBinaryClassModelQuality(BaseModel):
    f1: List[Distribution]
    accuracy: List[Distribution]
    precision: List[Distribution]
    recall: List[Distribution]
    f_measure: List[Distribution]
    weighted_precision: List[Distribution]
    weighted_recall: List[Distribution]
    weighted_f_measure: List[Distribution]
    weighted_true_positive_rate: List[Distribution]
    weighted_false_positive_rate: List[Distribution]
    true_positive_rate: List[Distribution]
    false_positive_rate: List[Distribution]
    area_under_roc: Optional[List[Distribution]] = None
    area_under_pr: Optional[List[Distribution]] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CurrentBinaryClassificationModelQuality(BaseModel):
    global_metrics: BinaryClassificationModelQuality
    grouped_metrics: GroupedBinaryClassModelQuality

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MultiClassModelQuality(ModelQuality):
    pass


class RegressionModelQuality(ModelQuality):
    pass
