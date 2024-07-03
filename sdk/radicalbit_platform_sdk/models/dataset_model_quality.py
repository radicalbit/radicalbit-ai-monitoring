from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ModelQuality(BaseModel):
    pass


class MetricsBase(BaseModel):
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
    area_under_roc: Optional[float] = None
    area_under_pr: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class BinaryClassificationModelQuality(ModelQuality, MetricsBase):
    true_positive_count: int
    false_positive_count: int
    true_negative_count: int
    false_negative_count: int


class Distribution(BaseModel):
    timestamp: str
    value: Optional[float] = None


class GroupedMetricsBase(BaseModel):
    f1: Optional[List[Distribution]] = None
    accuracy: Optional[List[Distribution]] = None
    precision: List[Distribution]
    recall: List[Distribution]
    f_measure: List[Distribution]
    weighted_precision: Optional[List[Distribution]] = None
    weighted_recall: Optional[List[Distribution]] = None
    weighted_f_measure: Optional[List[Distribution]] = None
    weighted_true_positive_rate: Optional[List[Distribution]] = None
    weighted_false_positive_rate: Optional[List[Distribution]] = None
    true_positive_rate: List[Distribution]
    false_positive_rate: List[Distribution]
    area_under_roc: Optional[List[Distribution]] = None
    area_under_pr: Optional[List[Distribution]] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CurrentBinaryClassificationModelQuality(ModelQuality):
    global_metrics: BinaryClassificationModelQuality
    grouped_metrics: GroupedMetricsBase

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ClassMetrics(BaseModel):
    class_name: str
    metrics: MetricsBase
    grouped_metrics: Optional[GroupedMetricsBase] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class GlobalMetrics(MetricsBase):
    confusion_matrix: List[List[int]]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MultiClassificationModelQuality(ModelQuality):
    classes: List[str]
    class_metrics: List[ClassMetrics]
    global_metrics: GlobalMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class RegressionModelQuality(ModelQuality):
    pass
