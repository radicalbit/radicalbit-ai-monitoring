from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List, Optional, Union


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
    type: str = "numerical"
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]
    histogram: Histogram

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)


class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = "categorical"
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class DataQuality(BaseModel):
    pass


class BinaryClassificationDataQuality(DataQuality):
    n_observations: int
    class_metrics: List[ClassMetrics]
    feature_metrics: List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class MultiClassDataQuality(DataQuality):
    pass


class RegressionDataQuality(DataQuality):
    pass
