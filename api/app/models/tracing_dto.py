from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TreeNode(BaseModel):
    name: str
    tokens: int
    duration: int
    children: List['TreeNode'] = Field(default_factory=list)


class SpanBasic(BaseModel):
    name: str
    span_id: str
    duration: int
    tokens: int
    created_at: str


class SpanDTO(SpanBasic):
    thread_id: Optional[UUID] = None
    attributes: dict
    error: Optional[str] = None


class TraceDTO(SpanBasic):
    spans: int
    projec_uuid: UUID
    number_of_errors: int
    tree: Optional[TreeNode] = None


class SessionDTO(BaseModel):
    session_uuid: UUID
    traces: int
    durations: int
    tokens: int
    number_of_errors: int
    created_at: str
