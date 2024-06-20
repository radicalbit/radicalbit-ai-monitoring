import uuid as uuid_lib
from enum import Enum
from radicalbit_platform_sdk.models.data_type import DataType
from radicalbit_platform_sdk.models.model_type import ModelType
from radicalbit_platform_sdk.models.column_definition import ColumnDefinition
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OutputType(BaseModel):
    prediction: ColumnDefinition
    prediction_proba: Optional[ColumnDefinition] = None
    output: List[ColumnDefinition]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class Granularity(str, Enum):
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class BaseModelDefinition(BaseModel):
    """A base class for model definition.

    Attributes:
        name: The name of the model.
        description: An optional description to explain something about the model.
        model_type: The type of the model
        data_type: It explanin the data type used by the model
        granularity: The window used to calculate aggregated metrics
        features: A list column representing the features set
        outputs: An OutputType definition to explaing the output of the model
        target: The column used to represent model's target
        timestamp: The column used to store the when prediction was done
        frameworks: An optional field to describe the frameworks used by the model
        algorithm: An optional field to ecplane the algorithm used by the model
    """

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


class CreateModel(BaseModelDefinition):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ModelDefinition(BaseModelDefinition):
    uuid: uuid_lib.UUID = Field(default_factory=lambda: uuid_lib.uuid4())
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class PaginatedModelDefinitions(BaseModel):
    items: List[ModelDefinition]

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
