import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.db.dao.model_dao import Model


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


class ColumnDefinition(BaseModel):
    name: str
    type: str

    def to_dict(self):
        return self.model_dump()


class OutputType(BaseModel):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    def to_dict(self):
        return self.model_dump()


class ModelIn(BaseModel):
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

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_model(model: Model):
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
        )
