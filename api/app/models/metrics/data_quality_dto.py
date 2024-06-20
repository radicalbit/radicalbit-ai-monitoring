from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.exceptions import MetricsInternalError
from app.models.job_status import JobStatus
from app.models.model_dto import ModelType


class MedianMetrics(BaseModel):
    perc_25: Optional[float] = None
    median: Optional[float] = None
    perc_75: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class MissingValue(BaseModel):
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class ClassMedianMetrics(BaseModel):
    name: str
    mean: Optional[float] = None
    median_metrics: MedianMetrics

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class Histogram(BaseModel):
    buckets: List[float]
    reference_values: List[int]
    current_values: Optional[List[int]] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class FeatureMetrics(BaseModel):
    feature_name: str
    type: str
    missing_value: MissingValue

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class NumericalFeatureMetrics(FeatureMetrics):
    type: str = 'numerical'
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    median_metrics: MedianMetrics
    class_median_metrics: List[ClassMedianMetrics]
    histogram: Histogram

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class CategoryFrequency(BaseModel):
    name: str
    count: int
    frequency: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class CategoricalFeatureMetrics(FeatureMetrics):
    type: str = 'categorical'
    category_frequency: List[CategoryFrequency]
    distinct_value: int

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class ClassMetrics(BaseModel):
    name: str
    count: int
    percentage: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class BinaryClassDataQuality(BaseModel):
    n_observations: int
    class_metrics: List[ClassMetrics]
    feature_metrics: List[Union[NumericalFeatureMetrics, CategoricalFeatureMetrics]]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
        protected_namespaces=(),
    )


class MultiClassDataQuality(BaseModel):
    pass


class RegressionDataQuality(BaseModel):
    pass


class DataQualityDTO(BaseModel):
    job_status: JobStatus
    data_quality: Optional[
        Union[BinaryClassDataQuality, MultiClassDataQuality, RegressionDataQuality]
    ]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
        protected_namespaces=(),
    )

    @staticmethod
    def from_dict(
        model_type: ModelType,
        job_status: JobStatus,
        data_quality_data: Optional[Dict],
    ):
        if not data_quality_data:
            return DataQualityDTO(
                job_status=job_status,
                data_quality=None,
            )
        match model_type:
            case ModelType.BINARY:
                binary_class_data_quality = BinaryClassDataQuality(**data_quality_data)
                return DataQualityDTO(
                    job_status=job_status,
                    data_quality=binary_class_data_quality,
                )
            case ModelType.MULTI_CLASS:
                multi_class_data_quality = MultiClassDataQuality(**data_quality_data)
                return DataQualityDTO(
                    job_status=job_status,
                    data_quality=multi_class_data_quality,
                )
            case ModelType.REGRESSION:
                regression_data_quality = RegressionDataQuality(**data_quality_data)
                return DataQualityDTO(
                    job_status=job_status,
                    data_quality=regression_data_quality,
                )
            case _:
                raise MetricsInternalError(f'Invalid model type {model_type}')
