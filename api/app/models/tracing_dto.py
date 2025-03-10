from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TreeNode(BaseModel):
    name: str
    tokens: int
    duration: int
    children: List['TreeNode'] = Field(default_factory=list)


class SpanBasic(BaseModel):
    name: str
    trace_id: Optional[str] = None
    span_id: str
    duration: int
    tokens: int
    created_at: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class SpanDTO(SpanBasic):
    session_uuid: Optional[UUID] = None
    attributes: dict
    error: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class TraceDTO(SpanBasic):
    spans: int
    project_uuid: UUID
    number_of_errors: int
    tree: Optional[TreeNode] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


class SessionDTO(BaseModel):
    session_uuid: UUID
    traces: int
    durations: int
    tokens: int
    number_of_errors: int
    created_at: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
