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

from metrics.drift_factory_pattern import DriftAlgorithmType


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


class FieldTypes(str, Enum):
    categorical = "categorical"
    numerical = "numerical"
    datetime = "datetime"


class ModelType(str, Enum):
    REGRESSION = "REGRESSION"
    BINARY = "BINARY"
    MULTI_CLASS = "MULTI_CLASS"
    TEXT_GENERATION = "TEXT_GENERATION"


class DataType(str, Enum):
    TABULAR = "TABULAR"
    TEXT = "TEXT"
    IMAGE = "IMAGE"


class Granularity(str, Enum):
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

class DriftMethod(BaseModel):
    name: DriftAlgorithmType
    threshold: Optional[float] = None
    p_value: Optional[float] = None


class ColumnDefinition(BaseModel):
    name: str
    type: SupportedTypes
    field_type: FieldTypes
    drift: Optional[DriftMethod] = None

    def is_numerical(self) -> bool:
        return self.field_type == FieldTypes.numerical

    def is_float(self) -> bool:
        return (
            self.field_type == FieldTypes.numerical
            and self.type == SupportedTypes.float
        )

    def is_int(self) -> bool:
        return (
            self.field_type == FieldTypes.numerical and self.type == SupportedTypes.int
        )

    def is_categorical(self) -> bool:
        return self.field_type == FieldTypes.categorical

    def is_datetime(self) -> bool:
        return self.field_type == FieldTypes.datetime


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
    features: Optional[List[ColumnDefinition]]
    outputs: Optional[OutputType]
    target: Optional[ColumnDefinition]
    timestamp: Optional[ColumnDefinition]
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

    def get_float_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_float()]

    def get_int_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_int()]

    def get_categorical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_categorical()]
