from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pyspark.sql.types import (
    StructType,
    StructField,
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

    def to_reference_spark_schema(self):
        """
        This will enforce float for target, prediction and prediction_proba if binary classification
        :return: the spark scheme of the reference dataset
        """

        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        if self.outputs.prediction_proba and self.model_type == ModelType.BINARY:
            enforce_float = [
                self.target.name,
                self.outputs.prediction.name,
                self.outputs.prediction_proba.name,
            ]
        elif self.model_type == ModelType.BINARY:
            enforce_float = [self.target.name, self.outputs.prediction.name]
        else:
            enforce_float = []
        return StructType(
            [
                StructField(
                    name=feature.name,
                    dataType=self.convert_types(feature.type),
                    nullable=False,
                )
                if feature.name not in enforce_float
                else StructField(
                    name=feature.name,
                    dataType=DoubleType(),
                    nullable=False,
                )
                for feature in all_features
            ]
        )

    # FIXME this must exclude target when we will have separate current and ground truth
    def to_current_spark_schema(self):
        """
        This will enforce float for target, prediction and prediction_proba
        :return: the spark scheme of the current dataset (in the future without target)
        """

        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        if self.outputs.prediction_proba and self.model_type == ModelType.BINARY:
            enforce_float = [
                self.target.name,
                self.outputs.prediction.name,
                self.outputs.prediction_proba.name,
            ]
        elif self.model_type == ModelType.BINARY:
            enforce_float = [self.target.name, self.outputs.prediction.name]
        else:
            enforce_float = []
        return StructType(
            [
                StructField(
                    name=feature.name,
                    dataType=self.convert_types(feature.type),
                    nullable=False,
                )
                if feature.name not in enforce_float
                else StructField(
                    name=feature.name,
                    dataType=DoubleType(),
                    nullable=False,
                )
                for feature in all_features
            ]
        )

    def get_numerical_variables_reference(self) -> List[ColumnDefinition]:
        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        return [feature for feature in all_features if feature.is_numerical()]

    def get_categorical_variables_reference(self) -> List[ColumnDefinition]:
        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        return [feature for feature in all_features if feature.is_categorical()]

    def get_datetime_variables_reference(self) -> List[ColumnDefinition]:
        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        return [feature for feature in all_features if feature.is_datetime()]

    def get_all_variables_reference(self) -> List[ColumnDefinition]:
        return self.features + [self.target] + [self.timestamp] + self.outputs.output

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_numerical_variables_current(self) -> List[ColumnDefinition]:
        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        return [feature for feature in all_features if feature.is_numerical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_categorical_variables_current(self) -> List[ColumnDefinition]:
        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        return [feature for feature in all_features if feature.is_categorical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_datetime_variables_current(self) -> List[ColumnDefinition]:
        all_features = (
            self.features + [self.target] + [self.timestamp] + self.outputs.output
        )
        return [feature for feature in all_features if feature.is_datetime()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_all_variables_current(self) -> List[ColumnDefinition]:
        return self.features + [self.target] + [self.timestamp] + self.outputs.output

    def get_numerical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_numerical()]

    def get_categorical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.features if feature.is_categorical()]
