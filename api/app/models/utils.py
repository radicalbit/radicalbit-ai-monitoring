from typing import Any, Optional

from app.models.inferred_schema_dto import SupportedTypes


def is_number(value: SupportedTypes):
    return value in (SupportedTypes.int, SupportedTypes.float)


def is_number_or_string(value: SupportedTypes):
    return value in (SupportedTypes.int, SupportedTypes.float, SupportedTypes.string)


def is_optional_float(value: Optional[SupportedTypes] = None) -> bool:
    return value in (None, SupportedTypes.float)


def is_none(value: Any) -> bool:
    return value is None
