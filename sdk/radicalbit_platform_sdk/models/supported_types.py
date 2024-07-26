from enum import Enum


class SupportedTypes(str, Enum):
    string = 'string'
    int = 'int'
    float = 'float'
    bool = 'bool'
    datetime = 'datetime'
