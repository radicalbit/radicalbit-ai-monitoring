from enum import Enum
from typing import List

from numpy import dtypes as npy_dtypes
from pandas.core.arrays import boolean, floating, integer, string_
from pandas.core.dtypes import dtypes as pd_dtypes
from pydantic import BaseModel, ConfigDict

from app.models.exceptions import UnsupportedSchemaException


class SupportedTypes(str, Enum):
    string = 'string'
    int = 'int'
    float = 'float'
    bool = 'bool'
    datetime = 'datetime'

    @staticmethod
    def cast(value) -> 'SupportedTypes':
        match type(value):
            case string_.StringDtype:
                return SupportedTypes.string
            case integer.Int64Dtype:
                return SupportedTypes.int
            case floating.Float64Dtype:
                return SupportedTypes.float
            case boolean.BooleanDtype:
                return SupportedTypes.bool
            case npy_dtypes.DateTime64DType:
                return SupportedTypes.datetime
            case pd_dtypes.DatetimeTZDtype:
                return SupportedTypes.datetime
        raise UnsupportedSchemaException(f'Unsupported type: {type(value)}')


class SchemaEntry(BaseModel):
    name: str
    type: SupportedTypes

    model_config = ConfigDict(arbitrary_types_allowed=True)


class InferredSchemaDTO(BaseModel):
    inferred_schema: List[SchemaEntry]
