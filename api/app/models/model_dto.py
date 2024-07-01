import datetime
from enum import Enum
from typing import List, Optional, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel

from app.db.dao.model_dao import Model
from app.models.inferred_schema_dto import SupportedTypes
from app.models.utils import is_none, is_number, is_number_or_string, is_optional_float


class ModelType(str, Enum):
    REGRESSION = 'REGRESSION'
    BINARY = 'BINARY'
    MULTI_CLASS = 'MULTI_CLASS'


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

    def to_dict(self):
        return self.model_dump()


class OutputType(BaseModel, validate_assignment=True):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def to_dict(self):
        return self.model_dump()


class ModelIn(BaseModel, validate_assignment=True):
    name: str
    description: Optional[str] = None
    model_type: ModelType
    data_type: DataType
    granularity: Granularity
    features: List[ColumnDefinition]
    outputs: OutputType
    target: ColumnDefinition
    timestamp: ColumnDefinition
    frameworks: Optional[str] = None
    algorithm: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @model_validator(mode='after')
    def validate_target(self) -> Self:
        checked_model_type: ModelType = self.model_type
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
            case _:
                raise ValueError('not supported type for model_type')

    @model_validator(mode='after')
    def validate_outputs(self) -> Self:
        checked_model_type: ModelType = self.model_type
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
            case _:
                raise ValueError('not supported type for model_type')

    @model_validator(mode='after')
    def timestamp_must_be_datetime(self) -> Self:
        if not self.timestamp.type == SupportedTypes.datetime:
            raise ValueError('timestamp must be a datetime')
        return self

    def to_model(self) -> Model:
        now = datetime.datetime.now(tz=datetime.UTC)
        return Model(
            name=self.name,
            description=self.description,
            model_type=self.model_type.value,
            data_type=self.data_type.value,
            granularity=self.granularity.value,
            features=[feature.to_dict() for feature in self.features],
            outputs=self.outputs.to_dict(),
            target=self.target.to_dict(),
            timestamp=self.timestamp.to_dict(),
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
    features: List[ColumnDefinition]
    outputs: OutputType
    target: ColumnDefinition
    timestamp: ColumnDefinition
    frameworks: Optional[str]
    algorithm: Optional[str]
    created_at: str
    updated_at: str
    latest_reference_uuid: Optional[UUID]
    latest_current_uuid: Optional[UUID]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_model(
        model: Model,
        latest_reference_uuid: Optional[UUID] = None,
        latest_current_uuid: Optional[UUID] = None,
    ):
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
        )
