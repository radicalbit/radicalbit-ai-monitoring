from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ModelQuality(BaseModel):
    pass


class Distribution(BaseModel):
    timestamp: str
    value: Optional[float] = None


class BaseClassificationMetrics(BaseModel):
    precision: Optional[float] = None
    recall: Optional[float] = None
    f_measure: Optional[float] = None
    true_positive_rate: Optional[float] = None
    false_positive_rate: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class GroupedBaseClassificationMetrics(BaseModel):
    precision: List[Distribution]
    recall: List[Distribution]
    f_measure: List[Distribution]
    true_positive_rate: List[Distribution]
    false_positive_rate: List[Distribution]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class AdditionalMetrics(BaseModel):
    f1: Optional[float] = None
    accuracy: Optional[float] = None
    weighted_precision: Optional[float] = None
    weighted_recall: Optional[float] = None
    weighted_f_measure: Optional[float] = None
    weighted_true_positive_rate: Optional[float] = None
    weighted_false_positive_rate: Optional[float] = None
    area_under_roc: Optional[float] = None
    area_under_pr: Optional[float] = None
    log_loss: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class AdditionalGroupedMetrics(GroupedBaseClassificationMetrics):
    f1: List[Distribution]
    accuracy: List[Distribution]
    weighted_precision: List[Distribution]
    weighted_recall: List[Distribution]
    weighted_f_measure: List[Distribution]
    weighted_true_positive_rate: List[Distribution]
    weighted_false_positive_rate: List[Distribution]
    area_under_roc: Optional[List[Distribution]] = None
    area_under_pr: Optional[List[Distribution]] = None
    log_loss: Optional[List[Distribution]] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class GlobalBinaryMetrics(BaseClassificationMetrics, AdditionalMetrics):
    true_positive_count: int
    false_positive_count: int
    true_negative_count: int
    false_negative_count: int

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class BinaryClassificationModelQuality(ModelQuality, GlobalBinaryMetrics):
    pass


class CurrentBinaryClassificationModelQuality(ModelQuality):
    global_metrics: GlobalBinaryMetrics
    grouped_metrics: AdditionalGroupedMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ClassMetrics(BaseModel):
    class_name: str
    metrics: BaseClassificationMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class AdditionalClassMetrics(ClassMetrics):
    grouped_metrics: GroupedBaseClassificationMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class GlobalMulticlassMetrics(AdditionalMetrics):
    confusion_matrix: List[List[int]]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MultiClassificationModelQuality(ModelQuality):
    classes: List[str]
    class_metrics: List[ClassMetrics]
    global_metrics: GlobalMulticlassMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CurrentMultiClassificationModelQuality(ModelQuality):
    classes: List[str]
    class_metrics: List[AdditionalClassMetrics]
    global_metrics: GlobalMulticlassMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class KsMetrics(BaseModel):
    p_value: Optional[float] = None
    statistic: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class Histogram(BaseModel):
    buckets: List[float]
    values: Optional[List[int]] = None


class RegressionLine(BaseModel):
    coefficient: Optional[float] = None
    intercept: Optional[float] = None


class ResidualsMetrics(BaseModel):
    ks: KsMetrics
    correlation_coefficient: Optional[float] = None
    histogram: Histogram
    standardized_residuals: List[float]
    predictions: List[float]
    targets: List[float]
    regression_line: RegressionLine

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class BaseRegressionMetrics(BaseModel):
    r2: Optional[float] = None
    mae: Optional[float] = None
    mse: Optional[float] = None
    variance: Optional[float] = None
    mape: Optional[float] = None
    rmse: Optional[float] = None
    adj_r2: Optional[float] = None
    residuals: ResidualsMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class GroupedBaseRegressionMetrics(BaseModel):
    r2: List[Distribution]
    mae: List[Distribution]
    mse: List[Distribution]
    variance: List[Distribution]
    mape: List[Distribution]
    rmse: List[Distribution]
    adj_r2: List[Distribution]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class RegressionModelQuality(ModelQuality, BaseRegressionMetrics):
    pass


class CurrentRegressionModelQuality(ModelQuality):
    global_metrics: BaseRegressionMetrics
    grouped_metrics: GroupedBaseRegressionMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
