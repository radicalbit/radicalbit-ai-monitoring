from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class LatenciesWidget(BaseModel):
    project_uuid: UUID
    session_uuid: Optional[UUID] = None
    span_name: Optional[str] = None
    p50_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class TraceCount(BaseModel):
    count: int
    start_date: datetime

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class TraceTimeseries(BaseModel):
    project_uuid: UUID
    from_datetime: datetime
    to_datetime: datetime
    n: int
    traces: list[TraceCount]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class TraceCountSession(BaseModel):
    count: int
    session_uuid: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class SessionsTraces(BaseModel):
    project_uuid: UUID
    from_datetime: datetime
    to_datetime: datetime
    traces: list[TraceCountSession]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )
