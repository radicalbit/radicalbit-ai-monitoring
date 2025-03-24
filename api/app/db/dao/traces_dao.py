from datetime import datetime
import logging
import re
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import (
    Integer,
    Row,
    RowMapping,
    String,
    and_,
    asc,
    desc,
    distinct,
    func,
    literal_column,
    not_,
    select,
    text,
)

from app.core import get_config
from app.db.clickhouse_database import ClickHouseDatabase
from app.db.tables.traces_table import Trace
from app.models.commons.order_type import OrderType
from app.models.exceptions import TraceSortColumnError

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceDAO:
    def __init__(self, database: ClickHouseDatabase):
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
                'duration',
                'created_at',
                'latest_trace_ts',
            ]:
                raise TraceSortColumnError(
                    message=f'Column {column_name} does not allow sorting'
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
                    Trace.service_name.label('project_uuid'),
                    Trace.parent_span_id,
                    Trace.span_attributes,
                    Trace.status_code,
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
                    func.sum(span_attrs_stmt.c.status_code == 'Error').label(
                        'number_of_errors'
                    ),
                )
                .group_by(span_attrs_stmt.c.session_uuid)
                .subquery()
            )

            stmt = (
                select(
                    parent_span_filter_stmt.c.project_uuid,
                    parent_span_filter_stmt.c.session_uuid,
                    func.min(parent_span_filter_stmt.c.timestamp)
                    .cast(String)
                    .label('created_at'),
                    func.max(parent_span_filter_stmt.c.timestamp)
                    .cast(String)
                    .label('latest_trace_ts'),
                    func.count(parent_span_filter_stmt.c.trace_id).label('traces'),
                    func.sum(parent_span_filter_stmt.c.duration).label('duration'),
                )
                .group_by(
                    parent_span_filter_stmt.c.project_uuid,
                    parent_span_filter_stmt.c.session_uuid,
                )
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

    def get_all_root_traces_by_project_uuid(
        self,
        project_uuid: UUID,
        trace_id: Optional[str] = None,
        session_uuid: Optional[str] = None,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ):
        def order_by_column_name(column_name: str) -> str:
            formatted_column_name = re.sub('(?=[A-Z])', '_', column_name).lower()
            if formatted_column_name not in [
                'spans',
                'duration',
                'completion_tokens',
                'prompt_tokens',
                'total_tokens',
                'number_of_errors',
                'created_at',
                'latest_span_ts',
            ]:
                raise TraceSortColumnError(
                    message=f'Column {column_name} does not allow sorting'
                )
            return formatted_column_name

        with self.db.begin_session() as session:
            # Base subquery to extract span attributes from traces with project_uuid filter
            base_spans = (
                select(
                    Trace.timestamp,
                    Trace.trace_id,
                    Trace.span_id,
                    Trace.service_name,
                    Trace.duration,
                    Trace.parent_span_id,
                    Trace.span_attributes,
                    Trace.status_code,
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
                .filter(Trace.service_name == str(project_uuid))
                .filter(
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    )
                )
            )

            # Add optional trace_id filter with "like" as search
            if trace_id:
                base_spans = base_spans.filter(Trace.trace_id.like(f'{trace_id}%'))

            # Add optional timestamp filters
            if from_timestamp:
                base_spans = base_spans.filter(Trace.timestamp >= from_timestamp)

            if to_timestamp:
                base_spans = base_spans.filter(Trace.timestamp <= to_timestamp)

            base_spans = base_spans.subquery().alias('base_spans')

            # Filter for root spans (those without parents)
            root_spans = select(base_spans).filter(base_spans.c.parent_span_id == '')

            # Add optional session_uuid filter with "like" as search
            if session_uuid:
                root_spans = root_spans.filter(
                    base_spans.c.session_uuid.like(f'{session_uuid}%')
                )

            root_spans = root_spans.subquery().alias('root_spans')

            # Aggregate token usage by trace
            token_usage = (
                select(
                    base_spans.c.service_name,
                    base_spans.c.trace_id,
                    func.sum(base_spans.c.completion_tokens.cast(Integer)).label(
                        'completion_tokens'
                    ),
                    func.sum(base_spans.c.prompt_tokens.cast(Integer)).label(
                        'prompt_tokens'
                    ),
                    func.sum(base_spans.c.total_tokens.cast(Integer)).label(
                        'total_tokens'
                    ),
                )
                .filter(
                    base_spans.c.completion_tokens != '',
                    base_spans.c.prompt_tokens != '',
                    base_spans.c.total_tokens != '',
                )
                .group_by(base_spans.c.service_name, base_spans.c.trace_id)
                .subquery()
                .alias('token_usage')
            )

            # Count errors by trace
            error_counts = (
                select(
                    base_spans.c.service_name,
                    base_spans.c.trace_id,
                    func.sum(base_spans.c.status_code == 'Error').label(
                        'number_of_errors'
                    ),
                )
                .group_by(base_spans.c.service_name, base_spans.c.trace_id)
                .subquery()
                .alias('error_count')
            )

            # Aggregate general trace metrics by trace
            trace_metrics = (
                select(
                    base_spans.c.service_name,
                    base_spans.c.trace_id,
                    base_spans.c.session_uuid,
                    func.min(base_spans.c.timestamp).cast(String).label('created_at'),
                    func.max(base_spans.c.timestamp)
                    .cast(String)
                    .label('latest_span_ts'),
                    func.count(base_spans.c.span_id).label('spans'),
                )
                .group_by(
                    base_spans.c.service_name,
                    base_spans.c.trace_id,
                    base_spans.c.session_uuid,
                )
                .subquery()
                .alias('trace_metrics')
            )

            # Aggregate duration trace metrics by trace
            duration_metrics = (
                select(
                    root_spans.c.service_name,
                    root_spans.c.trace_id,
                    root_spans.c.span_id,
                    func.sum(root_spans.c.duration).label('duration'),
                )
                .group_by(
                    root_spans.c.service_name,
                    root_spans.c.trace_id,
                    root_spans.c.span_id,
                )
                .subquery()
                .alias('duration_metrics')
            )

            # Combine trace metrics with token usage
            metrics_with_tokens = (
                select(
                    trace_metrics.c.service_name,
                    trace_metrics.c.trace_id,
                    trace_metrics.c.session_uuid,
                    trace_metrics.c.created_at,
                    trace_metrics.c.latest_span_ts,
                    trace_metrics.c.spans,
                    token_usage.c.completion_tokens,
                    token_usage.c.prompt_tokens,
                    token_usage.c.total_tokens,
                )
                .join(
                    token_usage,
                    and_(
                        trace_metrics.c.service_name == token_usage.c.service_name,
                        trace_metrics.c.trace_id == token_usage.c.trace_id,
                    ),
                )
                .subquery()
                .alias('metrics_with_tokens')
            )

            # Combine metrics_with_tokens with duration

            metrics_with_tokens_and_duration = (
                select(
                    metrics_with_tokens.c.service_name,
                    metrics_with_tokens.c.trace_id,
                    metrics_with_tokens.c.session_uuid,
                    metrics_with_tokens.c.created_at,
                    metrics_with_tokens.c.latest_span_ts,
                    metrics_with_tokens.c.spans,
                    metrics_with_tokens.c.completion_tokens,
                    metrics_with_tokens.c.prompt_tokens,
                    metrics_with_tokens.c.total_tokens,
                    duration_metrics.c.duration,
                    duration_metrics.c.span_id,
                )
                .join(
                    metrics_with_tokens,
                    and_(
                        duration_metrics.c.service_name
                        == metrics_with_tokens.c.service_name,
                        duration_metrics.c.trace_id == metrics_with_tokens.c.trace_id,
                    ),
                )
                .subquery()
                .alias('metrics_with_tokens_and_duration')
            )

            # Final query combining all metrics with error counts
            final_query = select(
                metrics_with_tokens_and_duration.c.service_name.label('project_uuid'),
                metrics_with_tokens_and_duration.c.trace_id,
                metrics_with_tokens_and_duration.c.session_uuid,
                metrics_with_tokens_and_duration.c.span_id,
                metrics_with_tokens_and_duration.c.spans,
                metrics_with_tokens_and_duration.c.duration,
                metrics_with_tokens_and_duration.c.completion_tokens,
                metrics_with_tokens_and_duration.c.prompt_tokens,
                metrics_with_tokens_and_duration.c.total_tokens,
                error_counts.c.number_of_errors,
                metrics_with_tokens_and_duration.c.created_at,
                metrics_with_tokens_and_duration.c.latest_span_ts,
            ).join(
                error_counts,
                and_(
                    metrics_with_tokens_and_duration.c.service_name
                    == error_counts.c.service_name,
                    metrics_with_tokens_and_duration.c.trace_id
                    == error_counts.c.trace_id,
                ),
            )

            if sort:
                final_query = (
                    final_query.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else final_query.order_by(desc(order_by_column_name(sort)))
                )

            return paginate(session, final_query, params)

    def count_distinct_traces_by_project_uuid(self, project_uuid: UUID) -> int:
        with self.db.begin_session() as session:
            stmt = select(func.count(func.distinct(Trace.trace_id))).where(
                Trace.service_name == str(project_uuid)
            )

            return session.execute(stmt).scalar()

    def get_trace_by_project_uuid_trace_id(
        self,
        project_uuid: UUID,
        trace_id: str,
    ):
        with self.db.begin_session() as session:
            traces = (
                select(
                    Trace.timestamp.label('created_at'),
                    Trace.trace_id,
                    Trace.span_id,
                    Trace.service_name.label('project_uuid'),
                    Trace.duration,
                    Trace.parent_span_id,
                    Trace.span_name,
                    Trace.status_code,
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
                    Trace.service_name == str(project_uuid), Trace.trace_id == trace_id
                )
                .filter(
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    )
                )
            )

            return session.execute(traces)

    def delete_traces_by_project_uuid_trace_id(
        self,
        project_uuid: UUID,
        trace_id: str,
    ):
        with self.db.begin_session() as session:
            count_query = (
                select(func.count())
                .select_from(Trace)
                .filter(
                    Trace.service_name == str(project_uuid),
                    Trace.trace_id == trace_id,
                )
            )
            initial_count = session.execute(count_query).scalar()

            if initial_count == 0:
                logger.info('No traces found to delete.')
                return 0

            delete_query = text("""
                    ALTER TABLE default.otel_traces DELETE
                    WHERE ServiceName = :project_uuid AND TraceId = :trace_id
                """)

            session.execute(
                delete_query,
                {'project_uuid': str(project_uuid), 'trace_id': trace_id},
            )
            session.commit()

            logger.info('Deleted %i rows for trace_id %s', initial_count, trace_id)
            return initial_count

    def delete_traces_by_project_uuid_session_uuid(
        self,
        project_uuid: UUID,
        session_uuid: UUID,
    ):
        with self.db.begin_session() as session:
            count_query = (
                select(func.count())
                .select_from(Trace)
                .filter(
                    Trace.service_name == str(project_uuid),
                )
                .filter(
                    text(
                        "SpanAttributes['traceloop.association.properties.session_uuid'] = :session_uuid"
                    ),
                )
            ).params(session_uuid=str(session_uuid))
            initial_count = session.execute(count_query).scalar()

            if initial_count == 0:
                logger.info('No traces found to delete.')
                return 0

            delete_query = text("""
                ALTER TABLE default.otel_traces DELETE
                WHERE ServiceName = :project_uuid
                AND SpanAttributes['traceloop.association.properties.session_uuid'] = :session_uuid
            """)

            session.execute(
                delete_query,
                {'project_uuid': str(project_uuid), 'session_uuid': str(session_uuid)},
            )
            session.commit()

            logger.info(
                'Deleted %i rows for session_uuid %s', initial_count, session_uuid
            )
            return initial_count

    def get_latencies_quantiles_for_root_traces_dashboard(
        self,
        project_uuid: UUID,
        from_timestamp: datetime,
        to_timestamp: datetime,
    ):
        """Return quantiles of root traces latencies grouped by project_uuid"""
        with self.db.begin_session() as session:
            traces_quantiles = (
                select(
                    Trace.service_name.label('project_uuid'),
                    func.quantile(0.50, Trace.duration).label('p50'),
                    func.quantile(0.90, Trace.duration).label('p90'),
                    func.quantile(0.95, Trace.duration).label('p95'),
                    func.quantile(0.99, Trace.duration).label('p99'),
                )
                .group_by(
                    Trace.service_name,
                )
                .filter(
                    Trace.service_name == str(project_uuid),
                    Trace.parent_span_id == '',
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    ),
                    Trace.timestamp >= from_timestamp,
                    Trace.timestamp <= to_timestamp,
                )
            )

            return session.execute(traces_quantiles).one_or_none()

    def get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
        self,
        project_uuid: UUID,
        from_timestamp: datetime,
        to_timestamp: datetime,
    ):
        """Return quantiles of root traces latencies grouped by project_uuid and session_uuid, so the quantiles of traces duration for each session"""
        with self.db.begin_session() as session:
            root_traces_with_duration = (
                select(
                    Trace.service_name.label('project_uuid'),
                    literal_column(
                        "SpanAttributes['traceloop.association.properties.session_uuid']"
                    ).label('session_uuid'),
                    Trace.duration,
                )
                .filter(
                    Trace.service_name == str(project_uuid),
                    Trace.parent_span_id == '',
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    ),
                    Trace.timestamp >= from_timestamp,
                    Trace.timestamp <= to_timestamp,
                )
                .subquery()
            )

            traces_quantiles = select(
                root_traces_with_duration.c.project_uuid,
                root_traces_with_duration.c.session_uuid,
                func.quantile(0.50, root_traces_with_duration.c.duration).label('p50'),
                func.quantile(0.90, root_traces_with_duration.c.duration).label('p90'),
                func.quantile(0.95, root_traces_with_duration.c.duration).label('p95'),
                func.quantile(0.99, root_traces_with_duration.c.duration).label('p99'),
            ).group_by(
                root_traces_with_duration.c.project_uuid,
                root_traces_with_duration.c.session_uuid,
            )

            return session.execute(traces_quantiles)

    def get_latencies_quantiles_for_span_leaf_dashboard(
        self,
        project_uuid: UUID,
        from_timestamp: datetime,
        to_timestamp: datetime,
    ):
        """Return quantiles of span leaf (so they are not parent of any span) latencies grouped by project_uuid and span name"""
        with self.db.begin_session() as session:
            span_that_are_parents = select(
                distinct(Trace.parent_span_id),
            ).filter(
                Trace.service_name == str(project_uuid),
                text(
                    "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                ),
            )

            traces_quantiles = (
                select(
                    Trace.service_name.label('project_uuid'),
                    Trace.span_name,
                    func.quantile(0.50, Trace.duration).label('p50'),
                    func.quantile(0.90, Trace.duration).label('p90'),
                    func.quantile(0.95, Trace.duration).label('p95'),
                    func.quantile(0.99, Trace.duration).label('p99'),
                )
                .group_by(
                    Trace.service_name,
                    Trace.span_name,
                )
                .filter(
                    Trace.service_name == str(project_uuid),
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    ),
                    not_(Trace.span_id.in_(span_that_are_parents)),
                    Trace.timestamp >= from_timestamp,
                    Trace.timestamp <= to_timestamp,
                )
            )

            return session.execute(traces_quantiles)

    def get_span_by_id(self, project_uuid: UUID, trace_id: str, span_id: str):
        with self.db.begin_session() as session:
            stmt = (
                select(
                    Trace.span_id,
                    Trace.span_name,
                    Trace.parent_span_id,
                    Trace.trace_id,
                    Trace.service_name,
                    Trace.duration,
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
                    Trace.span_attributes.label('attributes'),
                    Trace.status_message,
                    Trace.timestamp,
                    Trace.events,
                )
                .filter(
                    Trace.service_name == str(project_uuid),
                    Trace.trace_id == trace_id,
                    Trace.span_id == span_id,
                )
                .filter(
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    )
                )
            )
            return session.execute(stmt).one_or_none()

    def get_traces_by_time_dashboard(
        self,
        project_uuid: UUID,
        from_datetime: datetime,
        to_datetime: datetime,
        interval_size: int,
    ) -> list[RowMapping]:
        with self.db.begin_session() as session:
            filter_stmt = (
                select(
                    Trace.trace_id,
                    Trace.parent_span_id,
                    Trace.service_name,
                    Trace.timestamp,
                )
                .filter(
                    Trace.service_name == str(project_uuid),
                    Trace.parent_span_id == '',
                    Trace.timestamp >= from_datetime,
                    Trace.timestamp <= to_datetime,
                )
                .subquery()
            )
            min_ts = select(
                func.min(filter_stmt.c.timestamp).label('min_timestamp')
            ).cte('min_timestamp')
            min_timestamp_scalar = select(min_ts.c.min_timestamp).scalar_subquery()
            stmt = (
                select(
                    func.count(filter_stmt.c.trace_id).label('count'),
                    func.toStartOfInterval(
                        filter_stmt.c.timestamp,
                        func.toIntervalSecond(str(interval_size)),
                        min_timestamp_scalar,
                    ).label('start_date'),
                )
                .group_by(text('start_date'))
                .order_by(text('start_date'))
            )
            return list(session.execute(stmt).mappings())

    def get_sessions_traces(
        self, project_uuid: UUID, from_datetime: datetime, to_datetime: datetime
    ) -> list[RowMapping]:
        with self.db.begin_session() as session:
            filter_stmt = (
                select(
                    Trace.service_name.label('project_uuid'),
                    Trace.trace_id,
                    Trace.parent_span_id,
                    Trace.timestamp,
                    literal_column(
                        "SpanAttributes['traceloop.association.properties.session_uuid']"
                    ).label('session_uuid'),
                )
                .filter(
                    Trace.service_name == str(project_uuid),
                    Trace.parent_span_id == '',
                    Trace.timestamp >= from_datetime,
                    Trace.timestamp <= to_datetime,
                )
                .subquery()
            )
            stmt = (
                select(filter_stmt.c.session_uuid, func.count(filter_stmt.c.trace_id))
                .group_by(filter_stmt.c.session_uuid)
                .order_by(desc(func.count(filter_stmt.c.trace_id)))
            )
            return list(session.execute(stmt).mappings())
