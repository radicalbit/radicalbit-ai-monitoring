from enum import Enum


class DatasetType(str, Enum):
    REFERENCE = 'REFERENCE'
    CURRENT = 'CURRENT'
    COMPLETION = 'COMPLETION'
