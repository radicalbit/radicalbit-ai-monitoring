import datetime
from enum import Enum
from typing import List, Optional, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel

from app.db.dao.current_dataset_dao import CurrentDataset
from app.db.dao.model_dao import Model
from app.db.dao.reference_dataset_dao import ReferenceDataset
from app.db.tables.completion_dataset_table import CompletionDataset
from app.models.inferred_schema_dto import FieldType, SupportedTypes
from app.models.job_status import JobStatus
from app.models.metrics.percentages_dto import Percentages
from app.models.utils import is_none, is_number, is_number_or_string, is_optional_float


class ModelType(str, Enum):
    REGRESSION = 'REGRESSION'
    BINARY = 'BINARY'
    MULTI_CLASS = 'MULTI_CLASS'
    TEXT_GENERATION = 'TEXT_GENERATION'


class DataType(str, Enum):
    TABULAR = 'TABULAR'
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'


class Granularity(str, Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'


class ColumnDefinition(BaseModel, validate_assignment=True):
    name: str
    type: SupportedTypes
    field_type: FieldType

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def to_dict(self):
        return self.model_dump()

    @model_validator(mode='after')
    def validate_field_type(self) -> Self:
        match (self.type, self.field_type):
            case (SupportedTypes.datetime, FieldType.datetime):
                return self
            case (SupportedTypes.string, FieldType.categorical):
                return self
            case (SupportedTypes.bool, FieldType.categorical):
                return self
            case (SupportedTypes.int, FieldType.categorical):
                return self
            case (SupportedTypes.float, FieldType.categorical):
                return self
            case (SupportedTypes.int, FieldType.numerical):
                return self
            case (SupportedTypes.float, FieldType.numerical):
                return self
            case _:
                raise ValueError(
                    f'column {self.name} with type {self.type} can not have filed type {self.field_type}'
                )


class OutputType(BaseModel, validate_assignment=True):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def to_dict(self):
        return self.model_dump()


class ModelFeatures(BaseModel):
    features: List[ColumnDefinition]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class ModelIn(BaseModel, validate_assignment=True):
    uuid: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: Optional[List[ColumnDefinition]] = None
    outputs: Optional[OutputType] = None
    target: Optional[ColumnDefinition] = None
    timestamp: Optional[ColumnDefinition] = None
    frameworks: Optional[str] = None
    algorithm: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @model_validator(mode='after')
    def validate_fields(self) -> Self:
        checked_model_type = self.model_type
        if checked_model_type == ModelType.TEXT_GENERATION:
            if any([self.target, self.features, self.outputs, self.timestamp]):
                raise ValueError(
                    f'target, features, outputs and timestamp must not be provided for a {checked_model_type}'
                )
            return self
        if not self.features:
            raise ValueError(f'features must be provided for a {checked_model_type}')
        if not self.outputs:
            raise ValueError(f'outputs must be provided for a {checked_model_type}')
        if not self.target:
            raise ValueError(f'target must be provided for a {checked_model_type}')
        if not self.timestamp:
            raise ValueError(f'timestamp must be provided for a {checked_model_type}')

        return self

    @model_validator(mode='after')
    def validate_target(self) -> Self:
        checked_model_type = self.model_type
        match checked_model_type:
            case ModelType.BINARY:
                if not is_number(self.target.type):
                    raise ValueError(
                        f'target must be a number for a {checked_model_type}, has been provided [{self.target}]'
                    )
                return self
            case ModelType.MULTI_CLASS:
                if not is_number_or_string(self.target.type):
                    raise ValueError(
                        f'target must be a number or string for a {checked_model_type}, has been provided [{self.target}]'
                    )
                return self
            case ModelType.REGRESSION:
                if not is_number(self.target.type):
                    raise ValueError(
                        f'target must be a number for a {checked_model_type}, has been provided [{self.target}]'
                    )
                return self
            case ModelType.TEXT_GENERATION:
                return self
            case _:
                raise ValueError('not supported type for model_type')

    @model_validator(mode='after')
    def validate_outputs(self) -> Self:
        checked_model_type = self.model_type
        match checked_model_type:
            case ModelType.BINARY:
                if not is_number(self.outputs.prediction.type):
                    raise ValueError(
                        f'prediction must be a number for a {checked_model_type}, has been provided [{self.outputs.prediction}]'
                    )
                if not is_none(self.outputs.prediction_proba) and not is_optional_float(
                    self.outputs.prediction_proba.type
                ):
                    raise ValueError(
                        f'prediction_proba must be an optional float for a {checked_model_type}, has been provided [{self.outputs.prediction_proba}]'
                    )
                return self
            case ModelType.MULTI_CLASS:
                if not is_number_or_string(self.outputs.prediction.type):
                    raise ValueError(
                        f'prediction must be a number or string for a {checked_model_type}, has been provided [{self.outputs.prediction}]'
                    )
                if not is_none(self.outputs.prediction_proba) and not is_optional_float(
                    self.outputs.prediction_proba.type
                ):
                    raise ValueError(
                        f'prediction_proba must be an optional float for a {checked_model_type}, has been provided [{self.outputs.prediction_proba}]'
                    )
                return self
            case ModelType.REGRESSION:
                if not is_number(self.outputs.prediction.type):
                    raise ValueError(
                        f'prediction must be a number for a {checked_model_type}, has been provided [{self.outputs.prediction}]'
                    )
                if not is_none(self.outputs.prediction_proba) and not is_none(
                    self.outputs.prediction_proba.type
                ):
                    raise ValueError(
                        f'prediction_proba must be None for a {checked_model_type}, has been provided [{self.outputs.prediction_proba}]'
                    )
                return self
            case ModelType.TEXT_GENERATION:
                return self
            case _:
                raise ValueError('not supported type for model_type')

    @model_validator(mode='after')
    def timestamp_must_be_datetime(self) -> Self:
        if self.model_type == ModelType.TEXT_GENERATION:
            return self
        if not self.timestamp.type == SupportedTypes.datetime:
            raise ValueError('timestamp must be a datetime')
        return self

    def to_model(self) -> Model:
        now = datetime.datetime.now(tz=datetime.UTC)
        return Model(
            uuid=self.uuid,
            name=self.name,
            description=self.description,
            model_type=self.model_type.value,
            data_type=self.data_type.value,
            granularity=self.granularity.value,
            features=[feature.to_dict() for feature in self.features]
            if self.features
            else None,
            outputs=self.outputs.to_dict() if self.outputs else None,
            target=self.target.to_dict() if self.target else None,
            timestamp=self.timestamp.to_dict() if self.timestamp else None,
            frameworks=self.frameworks,
            algorithm=self.algorithm,
            created_at=now,
            updated_at=now,
        )


class ModelOut(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str]
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: Optional[List[ColumnDefinition]]
    outputs: Optional[OutputType]
    target: Optional[ColumnDefinition]
    timestamp: Optional[ColumnDefinition]
    frameworks: Optional[str]
    algorithm: Optional[str]
    created_at: str
    updated_at: str
    latest_reference_uuid: Optional[UUID]
    latest_current_uuid: Optional[UUID]
    latest_completion_uuid: Optional[UUID]
    latest_reference_job_status: Optional[JobStatus]
    latest_current_job_status: Optional[JobStatus]
    latest_completion_job_status: Optional[JobStatus]
    percentages: Optional[Percentages]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_model(
        model: Model,
        latest_reference_dataset: Optional[ReferenceDataset] = None,
        latest_current_dataset: Optional[CurrentDataset] = None,
        latest_completion_dataset: Optional[CompletionDataset] = None,
        percentages: Optional[Percentages] = None,
    ):
        latest_reference_uuid = None
        latest_current_uuid = None
        latest_completion_uuid = None
        latest_reference_job_status = None
        latest_current_job_status = None
        latest_completion_job_status = None

        if model.model_type == ModelType.TEXT_GENERATION:
            if latest_completion_dataset:
                latest_completion_uuid = latest_completion_dataset.uuid
                latest_completion_job_status = latest_completion_dataset.status
            else:
                latest_completion_job_status = JobStatus.MISSING_COMPLETION
        else:
            if latest_reference_dataset:
                latest_reference_uuid = latest_reference_dataset.uuid
                latest_reference_job_status = latest_reference_dataset.status
            else:
                latest_reference_job_status = JobStatus.MISSING_REFERENCE

            if latest_current_dataset:
                latest_current_uuid = latest_current_dataset.uuid
                latest_current_job_status = latest_current_dataset.status
            else:
                latest_current_job_status = JobStatus.MISSING_CURRENT

        return ModelOut(
            uuid=model.uuid,
            name=model.name,
            description=model.description,
            model_type=model.model_type,
            data_type=model.data_type,
            granularity=model.granularity,
            features=model.features,
            outputs=model.outputs,
            target=model.target,
            timestamp=model.timestamp,
            frameworks=model.frameworks,
            algorithm=model.algorithm,
            created_at=str(model.created_at),
            updated_at=str(model.updated_at),
            latest_reference_uuid=latest_reference_uuid,
            latest_current_uuid=latest_current_uuid,
            latest_completion_uuid=latest_completion_uuid,
            latest_reference_job_status=latest_reference_job_status,
            latest_current_job_status=latest_current_job_status,
            latest_completion_job_status=latest_completion_job_status,
            percentages=percentages,
        )
