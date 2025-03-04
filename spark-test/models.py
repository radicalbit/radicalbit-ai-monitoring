from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from uuid import UUID


class FieldTypes(str, Enum):
    categorical = "categorical"
    numerical = "numerical"
    datetime = "datetime"


class DriftAlgorithmType(str, Enum):
    HELLINGER = "HELLINGER"
    WASSERSTEIN = "WASSERSTEIN"
    KS = "KS"
    JS = "JS"
    PSI = "PSI"
    CHI2 = "CHI2"
    KL = "KULLBACK"


class DriftMethod(BaseModel):
    name: DriftAlgorithmType
    threshold: Optional[float] = None
    p_value: Optional[float] = None


class SupportedTypes(str, Enum):
    string = "string"
    int = "int"
    float = "float"
    bool = "bool"
    datetime = "datetime"


class ColumnDefinition(BaseModel):
    name: str
    type: SupportedTypes
    field_type: FieldTypes
    drift: Optional[List[DriftMethod]] = None


class OutputType(BaseModel):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]


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
