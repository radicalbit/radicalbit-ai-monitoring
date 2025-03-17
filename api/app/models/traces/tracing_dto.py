from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel


class TreeNode(BaseModel):
    span_name: str
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    duration: int = Field(exclude=True)
    number_of_errors: int
    created_at: str
    children: List['TreeNode'] = Field(default_factory=list)

    @computed_field
    def durations_ms(self) -> float:
        return self.duration / 1_000_000

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )


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


class TraceDTO(BaseModel):
    project_uuid: UUID
    trace_id: str
    span_id: str
    session_uuid: UUID
    spans: int
    duration: int = Field(exclude=True)
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0
    number_of_errors: int
    created_at: str
    latest_span_ts: str
    tree: Optional[TreeNode] = None

    @computed_field
    def duration_ms(self) -> float:
        return self.duration / 1_000_000

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )

    @staticmethod
    def convert_traces_to_dto(
        traces: List[Dict[str, Any]], project_uuid: UUID
    ) -> 'TraceDTO':
        # Create a mapping of span_id to trace
        span_map = {trace['span_id']: trace for trace in traces}

        # Find the root trace (the one without parent_span_id)
        root_trace = next(trace for trace in traces if not trace['parent_span_id'])

        # Count spans
        num_spans = len(traces)

        # Calculate total tokens, errors, and find latest timestamp
        total_completion_tokens = 0
        total_prompt_tokens = 0
        total_tokens = 0
        total_errors = 0
        latest_timestamp = root_trace['created_at']

        for trace in traces:
            # Count tokens if available
            if trace['completion_tokens'] and trace['completion_tokens'] != '':
                total_completion_tokens += int(trace['completion_tokens'])
            if trace['prompt_tokens'] and trace['prompt_tokens'] != '':
                total_prompt_tokens += int(trace['prompt_tokens'])
            if trace['total_tokens'] and trace['total_tokens'] != '':
                total_tokens += int(trace['total_tokens'])

            # Count errors
            total_errors += 1 if trace['status_code'] == 'Error' else 0

            # Find latest timestamp
            if trace['created_at'] > latest_timestamp:
                latest_timestamp = trace['created_at']

        # Function to build tree recursively
        def build_tree(span_id: str) -> TreeNode:
            trace = span_map[span_id]

            # Count errors for this span
            span_error = 1 if trace['status_code'] == 'Error' else 0

            # Convert token values
            completion_tokens = (
                int(trace['completion_tokens'])
                if trace['completion_tokens'] and trace['completion_tokens'] != ''
                else 0
            )
            prompt_tokens = (
                int(trace['prompt_tokens'])
                if trace['prompt_tokens'] and trace['prompt_tokens'] != ''
                else 0
            )
            total_tokens_span = (
                int(trace['total_tokens'])
                if trace['total_tokens'] and trace['total_tokens'] != ''
                else 0
            )

            # Create node
            node = TreeNode(
                span_name=trace['span_name'],
                completion_tokens=completion_tokens,
                prompt_tokens=prompt_tokens,
                total_tokens=total_tokens_span,
                duration=trace['duration'],
                number_of_errors=span_error,
                created_at=str(trace['created_at']),
                children=[],
            )

            # Find children
            children_spans = [
                t['span_id'] for t in traces if t['parent_span_id'] == span_id
            ]
            for child_span_id in children_spans:
                node.children.append(build_tree(child_span_id))

            return node

        # Build the tree starting from root
        tree = build_tree(root_trace['span_id'])

        # Create and return the TraceDTO
        return TraceDTO(
            project_uuid=project_uuid,
            trace_id=root_trace['trace_id'],
            span_id=root_trace['span_id'],
            session_uuid=UUID(root_trace['session_uuid']),
            spans=num_spans,
            duration=root_trace['duration'],
            completion_tokens=total_completion_tokens,
            prompt_tokens=total_prompt_tokens,
            total_tokens=total_tokens,
            number_of_errors=total_errors,
            created_at=str(root_trace['created_at']),
            latest_span_ts=str(latest_timestamp),
            tree=tree,
        )


class SessionDTO(BaseModel):
    project_uuid: UUID
    session_uuid: UUID
    traces: int
    durations: int = Field(exclude=True)
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
