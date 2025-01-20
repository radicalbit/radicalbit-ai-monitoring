from typing import List, Dict, Optional

from pydantic import BaseModel, ConfigDict


class MedianMetrics(BaseModel):
    perc_25: float
    median: float
    perc_75: float

    model_config = ConfigDict(ser_json_inf_nan="null")


class MissingValue(BaseModel):
    count: int
    percentage: float

    model_config = ConfigDict(ser_json_inf_nan="null")


class ClassMedianMetrics(BaseModel):
    name: str
    mean: float
    median_metrics: MedianMetrics

    model_config = ConfigDict(ser_json_inf_nan="null")


class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue


class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None

    model_config = ConfigDict(ser_json_inf_nan="null")


class NumericalFeatureMetrics(FeatureMetrics):
    type: str = "numerical"
    mean: float
    std: float
    min: float
    max: float
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]
    histogram: Histogram

    model_config = ConfigDict(ser_json_inf_nan="null")

    @classmethod
    def from_dict(
        cls,
        feature_name: str,
        global_dict: Dict,
        histogram: Histogram,
    ) -> "NumericalFeatureMetrics":
        return NumericalFeatureMetrics(
            feature_name=feature_name,
            missing_value=MissingValue(
                count=global_dict.get("missing_values"),
                percentage=global_dict.get("missing_values_perc"),
            ),
            mean=global_dict.get("mean"),
            std=global_dict.get("std"),
            min=global_dict.get("min"),
            max=global_dict.get("max"),
            median_metrics=MedianMetrics(
                median=global_dict.get("median"),
                perc_25=global_dict.get("perc_25"),
                perc_75=global_dict.get("perc_75"),
            ),
            class_median_metrics=[],
            histogram=histogram,
        )


class NumericalTargetMetrics(FeatureMetrics):
    type: str = "numerical"
    mean: float
    std: float
    min: float
    max: float
    median_metrics: MedianMetrics
    histogram: Histogram

    model_config = ConfigDict(ser_json_inf_nan="null")

    @classmethod
    def from_dict(
        cls,
        feature_name: str,
        global_dict: Dict,
        histogram: Histogram,
    ) -> "NumericalTargetMetrics":
        return NumericalTargetMetrics(
            feature_name=feature_name,
            missing_value=MissingValue(
                count=global_dict.get("missing_values"),
                percentage=global_dict.get("missing_values_perc"),
            ),
            mean=global_dict.get("mean"),
            std=global_dict.get("std"),
            min=global_dict.get("min"),
            max=global_dict.get("max"),
            median_metrics=MedianMetrics(
                median=global_dict.get("median"),
                perc_25=global_dict.get("perc_25"),
                perc_75=global_dict.get("perc_75"),
            ),
            histogram=histogram,
        )


class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: float

    model_config = ConfigDict(ser_json_inf_nan="null")


class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = "categorical"
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(ser_json_inf_nan="null")

    @classmethod
    def from_dict(
        cls, feature_name: str, global_metrics: Dict, categories_metrics: Dict, prefix_id: str
    ) -> "CategoricalFeatureMetrics":
        count: Dict = categories_metrics.get(f"{prefix_id}_count")
        freq: Dict = categories_metrics.get(f"{prefix_id}_freq")
        return CategoricalFeatureMetrics(
            feature_name=feature_name,
            missing_value=MissingValue(
                count=global_metrics.get("missing_values"),
                percentage=global_metrics.get("missing_values_perc"),
            ),
            distinct_value=global_metrics.get("distinct_values"),
            category_frequency=[
                CategoryFrequency(
                    name=str(k), count=count.get(k), frequency=freq.get(k)
                )
                for k in count.keys()
            ],
        )


# Number and percentage of true and false
class ClassMetrics(BaseModel):
    name: str
    count: int
    percentage: float

    model_config = ConfigDict(ser_json_inf_nan="null")


class BinaryClassDataQuality(BaseModel):
    n_observations: int
    class_metrics: List[ClassMetrics]
    class_metrics_prediction: List[ClassMetrics]
    feature_metrics: List[FeatureMetrics]


class MultiClassDataQuality(BaseModel):
    n_observations: int
    class_metrics: List[ClassMetrics]
    class_metrics_prediction: List[ClassMetrics]
    feature_metrics: List[FeatureMetrics]


class RegressionDataQuality(BaseModel):
    n_observations: int
    target_metrics: NumericalTargetMetrics
    feature_metrics: List[FeatureMetrics]
