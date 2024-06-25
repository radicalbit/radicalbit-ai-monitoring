from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pyspark.sql.types import (
    StringType,
    DoubleType,
    IntegerType,
    TimestampType,
)


class JobStatus(str, Enum):
    IMPORTING = "IMPORTING"
    SUCCEEDED = "SUCCEEDED"
    ERROR = "ERROR"


class SupportedTypes(str, Enum):
    string = "string"
    int = "int"
    float = "float"
    bool = "bool"
    datetime = "datetime"


class ModelType(str, Enum):
    REGRESSION = "REGRESSION"
    BINARY = "BINARY"
    MULTI_CLASS = "MULTI_CLASS"


class DataType(str, Enum):
    TABULAR = "TABULAR"
    TEXT = "TEXT"
    IMAGE = "IMAGE"


class Granularity(str, Enum):
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class ColumnDefinition(BaseModel):
    name: str
    type: SupportedTypes

    def is_numerical(self) -> bool:
        return self.type == SupportedTypes.float or self.type == SupportedTypes.int

    def is_categorical(self) -> bool:
        return self.type == SupportedTypes.string or self.type == SupportedTypes.bool

    def is_datetime(self) -> bool:
        return self.type == SupportedTypes.datetime


class OutputType(BaseModel):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]


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

    @staticmethod
    def convert_types(t: str):
        match t:
            case SupportedTypes.string:
                return StringType()
            case SupportedTypes.float:
                return DoubleType()
            case SupportedTypes.int:
                return IntegerType()
            case SupportedTypes.bool:
                return StringType()
            # TODO maybe we want to discriminate between DateType (only the date without the time) and Timestamp
            case SupportedTypes.datetime:
                return TimestampType()

    def get_numerical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_numerical()]

    def get_categorical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_categorical()]
