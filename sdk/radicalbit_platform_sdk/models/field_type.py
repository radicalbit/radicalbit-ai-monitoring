from enum import Enum

from radicalbit_platform_sdk.models.supported_types import SupportedTypes


class FieldType(str, Enum):
    categorical = 'categorical'
    numerical = 'numerical'
    datetime = 'datetime'

    @staticmethod
    def from_supported_type(value: SupportedTypes) -> 'FieldType':
        match value:
            case SupportedTypes.datetime:
                return FieldType.datetime
            case SupportedTypes.int:
                return FieldType.numerical
            case SupportedTypes.float:
                return FieldType.numerical
            case SupportedTypes.bool:
                return FieldType.categorical
            case SupportedTypes.string:
                return FieldType.categorical
