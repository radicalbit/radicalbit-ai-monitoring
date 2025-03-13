import re
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import (
    Integer,
    Row,
    String,
    asc,
    desc,
    func,
    literal_column,
    select,
    text,
)

from app.db.database import Database
from app.db.tables.traces_table import Trace
from app.models.commons.order_type import OrderType
from app.models.exceptions import TraceSortColumnError


class TraceDAO:
    def __init__(self, database: Database):
        self.db = database

    def get_all_sessions(
        self,
        project_uuid: UUID,
        params: Optional[Params] = None,
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[Row]:
        def order_by_column_name(column_name: str) -> str:
            formatted_column_name = re.sub('(?=[A-Z])', '_', column_name).lower()
            if formatted_column_name not in [
                'traces',
                'durations',
                'created_at',
                'latest_trace_ts',
            ]:
                raise TraceSortColumnError(
                    message='Column passed does not allow sorting'
                )
            return formatted_column_name

        if params is None:
            params = Params()

        with self.db.begin_session() as session:
            span_attrs_stmt = (
                select(
                    Trace.timestamp,
                    Trace.trace_id,
                    Trace.duration,
                    Trace.service_name,
                    Trace.parent_span_id,
                    Trace.span_attributes,
                    Trace.events_attributes,
                    literal_column(
                        "SpanAttributes['traceloop.association.properties.session_uuid']"
                    ).label('session_uuid'),
                    literal_column(
                        "SpanAttributes['gen_ai.usage.completion_tokens']"
                    ).label('completion_tokens'),
                    literal_column(
                        "SpanAttributes['gen_ai.usage.prompt_tokens']"
                    ).label('prompt_tokens'),
                    literal_column("SpanAttributes['llm.usage.total_tokens']").label(
                        'total_tokens'
                    ),
                )
                .filter(
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    ),
                    Trace.service_name == str(project_uuid),
                )
                .subquery()
            )

            parent_span_filter_stmt = (
                select(span_attrs_stmt)
                .filter(span_attrs_stmt.c.parent_span_id == '')
                .subquery()
            )

            tokens_count_stmt = (
                select(
                    span_attrs_stmt.c.session_uuid,
                    func.sum(span_attrs_stmt.c.completion_tokens.cast(Integer)).label(
                        'completion_tokens'
                    ),
                    func.sum(span_attrs_stmt.c.prompt_tokens.cast(Integer)).label(
                        'prompt_tokens'
                    ),
                    func.sum(span_attrs_stmt.c.total_tokens.cast(Integer)).label(
                        'total_tokens'
                    ),
                )
                .filter(
                    span_attrs_stmt.c.completion_tokens != '',
                    span_attrs_stmt.c.prompt_tokens != '',
                    span_attrs_stmt.c.total_tokens != '',
                )
                .group_by(span_attrs_stmt.c.session_uuid)
                .subquery()
            )

            errors_stmt = (
                select(
                    span_attrs_stmt.c.session_uuid,
                    func.sum(
                        func.length(span_attrs_stmt.c.events_attributes) > 0
                    ).label('number_of_errors'),
                )
                .group_by(span_attrs_stmt.c.session_uuid)
                .subquery()
            )

            stmt = (
                select(
                    parent_span_filter_stmt.c.session_uuid,
                    func.min(parent_span_filter_stmt.c.timestamp)
                    .cast(String)
                    .label('created_at'),
                    func.max(parent_span_filter_stmt.c.timestamp)
                    .cast(String)
                    .label('latest_trace_ts'),
                    func.count(parent_span_filter_stmt.c.trace_id).label('traces'),
                    func.sum(parent_span_filter_stmt.c.duration).label('durations'),
                )
                .group_by(parent_span_filter_stmt.c.session_uuid)
                .subquery()
            )

            join_stmt = (
                select(stmt, tokens_count_stmt)
                .join(
                    tokens_count_stmt,
                    stmt.c.session_uuid == tokens_count_stmt.c.session_uuid,
                )
                .subquery()
            )

            final_join = select(join_stmt, errors_stmt).join(
                errors_stmt, join_stmt.c.session_uuid == errors_stmt.c.session_uuid
            )

            if sort:
                final_join = (
                    final_join.order_by(asc(text(order_by_column_name(sort))))
                    if order == OrderType.ASC
                    else final_join.order_by(desc(text(order_by_column_name(sort))))
                )

            return paginate(session, final_join, params)
