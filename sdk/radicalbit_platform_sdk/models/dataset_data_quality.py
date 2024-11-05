from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ClassMetrics(BaseModel):
    name: str
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)


class MedianMetrics(BaseModel):
    perc_25: Optional[float] = None
    median: Optional[float] = None
    perc_75: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MissingValue(BaseModel):
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)


class ClassMedianMetrics(BaseModel):
    name: str
    mean: Optional[float] = None
    median_metrics: MedianMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class NumericalFeatureMetrics(FeatureMetrics):
    type: str = 'numerical'
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]
    histogram: Histogram

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class NumericalTargetMetrics(FeatureMetrics):
    type: str = 'numerical'
    mean: float
    std: float
    min: float
    max: float
    median_metrics: MedianMetrics
    histogram: Histogram

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)


class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = 'categorical'
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class DataQuality(BaseModel):
    pass


class ClassificationDataQuality(DataQuality):
    n_observations: int
    class_metrics: List[ClassMetrics]
    class_metrics_prediction: List[ClassMetrics]
    feature_metrics: List[NumericalFeatureMetrics | CategoricalFeatureMetrics]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class RegressionDataQuality(DataQuality):
    n_observations: int
    target_metrics: NumericalTargetMetrics
    feature_metrics: List[NumericalFeatureMetrics | CategoricalFeatureMetrics]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
