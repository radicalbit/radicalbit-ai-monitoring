from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel


class TreeNode(BaseModel):
    name: str
    tokens: int
    duration: int
    children: List['TreeNode'] = Field(default_factory=list)


class SpanBasic(BaseModel):
    name: str
    trace_id: str
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
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    number_of_errors: int
    created_at: str
    latest_trace_ts: str

    @computed_field
    def durations_ms(self) -> float:
        return self.durations / 1_000_000

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )
