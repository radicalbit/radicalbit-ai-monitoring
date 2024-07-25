from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from radicalbit_platform_sdk.models.field_type import FieldType
from radicalbit_platform_sdk.models.supported_types import SupportedTypes


class ColumnDefinition(BaseModel, validate_assignment=True):
    name: str
    type: SupportedTypes
    field_type: FieldType = Field(alias='fieldType')

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
