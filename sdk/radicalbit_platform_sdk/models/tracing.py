from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Session(BaseModel):
    project_uuid: UUID
    session_uuid: UUID
    traces: int
    duration_ms: float
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    number_of_errors: int
    created_at: str
    latest_trace_ts: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class TreeNode(BaseModel):
    span_name: str
    span_id: str
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    durations_ms: float
    number_of_errors: int
    created_at: str
    children: List['TreeNode'] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class Trace(BaseModel):
    project_uuid: UUID
    trace_id: str
    span_id: str
    session_uuid: UUID
    spans: int
    duration_ms: float
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    number_of_errors: int
    created_at: str
    latest_span_ts: str
    tree: Optional[TreeNode] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class ErrorEvents(BaseModel):
    timestamp: Optional[datetime] = None
    name: Optional[str] = None
    attributes: Optional[dict] = None

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class Span(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    trace_id: str
    project_uuid: UUID
    durations_ms: float
    session_uuid: UUID
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    attributes: dict
    created_at: str
    status_message: Optional[str] = None
    error_events: list[ErrorEvents]

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
