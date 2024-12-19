from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.dataset_type import DatasetType
from app.models.exceptions import MetricsInternalError
from app.models.job_status import JobStatus
from app.models.model_dto import ModelType


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


class BinaryClassificationModelQuality(GlobalBinaryMetrics):
    pass


class CurrentBinaryClassificationModelQuality(BaseModel):
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


class MultiClassificationModelQuality(BaseModel):
    classes: List[str]
    class_metrics: List[ClassMetrics]
    global_metrics: GlobalMulticlassMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CurrentMultiClassificationModelQuality(BaseModel):
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


class RegressionModelQuality(BaseRegressionMetrics):
    pass


class CurrentRegressionModelQuality(BaseModel):
    global_metrics: BaseRegressionMetrics
    grouped_metrics: GroupedBaseRegressionMetrics

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class TokenProb(BaseModel):
    prob: float
    token: str


class TokenData(BaseModel):
    id: str
    message_content: str
    probs: List[TokenProb]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MeanPerFile(BaseModel):
    prob_tot_mean: float
    perplex_tot_mean: float

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class MeanPerPhrase(BaseModel):
    id: str
    prob_per_phrase: float
    perplex_per_phrase: float

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CompletionTextGenerationModelQuality(BaseModel):
    tokens: List[TokenData]
    mean_per_file: List[MeanPerFile]
    mean_per_phrase: List[MeanPerPhrase]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ModelQualityDTO(BaseModel):
    job_status: JobStatus
    model_quality: Optional[
        BinaryClassificationModelQuality
        | CurrentBinaryClassificationModelQuality
        | MultiClassificationModelQuality
        | CurrentMultiClassificationModelQuality
        | RegressionModelQuality
        | CurrentRegressionModelQuality
        | CompletionTextGenerationModelQuality
    ]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    @staticmethod
    def from_dict(
        dataset_type: DatasetType,
        model_type: ModelType,
        job_status: JobStatus,
        model_quality_data: Optional[Dict],
    ) -> 'ModelQualityDTO':
        """Create a ModelQualityDTO from a dictionary of data."""
        if not model_quality_data:
            return ModelQualityDTO(
                job_status=job_status,
                model_quality=None,
            )

        model_quality = ModelQualityDTO._create_model_quality(
            model_type=model_type,
            dataset_type=dataset_type,
            model_quality_data=model_quality_data,
        )

        return ModelQualityDTO(
            job_status=job_status,
            model_quality=model_quality,
        )

    @staticmethod
    def _create_model_quality(
        model_type: ModelType,
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ):
        """Create a specific model quality instance based on model type and dataset type."""
        if model_type == ModelType.BINARY:
            return ModelQualityDTO._create_binary_model_quality(
                dataset_type=dataset_type,
                model_quality_data=model_quality_data,
            )
        if model_type == ModelType.MULTI_CLASS:
            return ModelQualityDTO._create_multiclass_model_quality(
                dataset_type=dataset_type,
                model_quality_data=model_quality_data,
            )
        if model_type == ModelType.REGRESSION:
            return ModelQualityDTO._create_regression_model_quality(
                dataset_type=dataset_type, model_quality_data=model_quality_data
            )
        if model_type == ModelType.TEXT_GENERATION:
            return ModelQualityDTO._create_text_generation_model_quality(
                dataset_type=dataset_type, model_quality_data=model_quality_data
            )
        raise MetricsInternalError(f'Invalid model type {model_type}')

    @staticmethod
    def _create_binary_model_quality(
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> BinaryClassificationModelQuality | CurrentBinaryClassificationModelQuality:
        """Create a binary model quality instance based on dataset type."""
        if dataset_type == DatasetType.REFERENCE:
            return BinaryClassificationModelQuality(**model_quality_data)
        if dataset_type == DatasetType.CURRENT:
            return CurrentBinaryClassificationModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid dataset type {dataset_type}')

    @staticmethod
    def _create_multiclass_model_quality(
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> MultiClassificationModelQuality | CurrentMultiClassificationModelQuality:
        """Create a multiclass model quality instance based on dataset type."""
        if dataset_type == DatasetType.REFERENCE:
            return MultiClassificationModelQuality(**model_quality_data)
        if dataset_type == DatasetType.CURRENT:
            return CurrentMultiClassificationModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid dataset type {dataset_type}')

    @staticmethod
    def _create_regression_model_quality(
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> RegressionModelQuality | CurrentRegressionModelQuality:
        """Create a regression model quality instance based on dataset type."""
        if dataset_type == DatasetType.REFERENCE:
            return RegressionModelQuality(**model_quality_data)
        if dataset_type == DatasetType.CURRENT:
            return CurrentRegressionModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid dataset type {dataset_type}')

    @staticmethod
    def _create_text_generation_model_quality(
        dataset_type: DatasetType,
        model_quality_data: Dict,
    ) -> CompletionTextGenerationModelQuality:
        """Create a text generation model quality instance based on dataset type."""
        if dataset_type == DatasetType.COMPLETION:
            return CompletionTextGenerationModelQuality(**model_quality_data)
        raise MetricsInternalError(f'Invalid dataset type {dataset_type}')
