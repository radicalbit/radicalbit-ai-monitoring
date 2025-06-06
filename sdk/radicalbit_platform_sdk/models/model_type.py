from enum import Enum


class ModelType(str, Enum):
    REGRESSION = 'REGRESSION'
    BINARY = 'BINARY'
    MULTI_CLASS = 'MULTI_CLASS'
    TEXT_GENERATION = 'TEXT_GENERATION'
