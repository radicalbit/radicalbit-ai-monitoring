from typing import Dict, List, Optional

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


class ClassificationDataQuality(BaseModel):
    n_observations: int
    class_metrics: List[ClassMetrics]
    feature_metrics: List[NumericalFeatureMetrics | CategoricalFeatureMetrics]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
        protected_namespaces=(),
    )


class RegressionDataQuality(BaseModel):
    pass


class DataQualityDTO(BaseModel):
    job_status: JobStatus
    data_quality: Optional[ClassificationDataQuality | RegressionDataQuality]

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
    ) -> 'DataQualityDTO':
        """
        Create a DataQualityDTO from a dictionary of data.
        """
        if not data_quality_data:
            return DataQualityDTO(
                job_status=job_status,
                data_quality=None,
            )

        data_quality = DataQualityDTO._create_data_quality(
            model_type=model_type,
            data_quality_data=data_quality_data,
        )

        return DataQualityDTO(
            job_status=job_status,
            data_quality=data_quality,
        )

    @staticmethod
    def _create_data_quality(
        model_type: ModelType,
        data_quality_data: Dict,
    ) -> ClassificationDataQuality | RegressionDataQuality:
        """
        Create a specific data quality instance based on the model type.
        """
        if model_type in {ModelType.BINARY, ModelType.MULTI_CLASS}:
            return ClassificationDataQuality(**data_quality_data)
        elif model_type == ModelType.REGRESSION:
            return RegressionDataQuality(**data_quality_data)
        else:
            raise MetricsInternalError(f'Invalid model type {model_type}')
