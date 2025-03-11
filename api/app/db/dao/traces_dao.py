from sqlalchemy import String, func, literal_column, select, text

from app.db.database import Database
from app.db.tables.traces_table import Traces


class TraceDAO:
    def __init__(self, database: Database):
        self.db = database

    def get_all_sessions(self):
        with self.db.begin_session() as session:
            inner_stmt = (
                select(
                    Traces.timestamp,
                    Traces.trace_id,
                    Traces.duration,
                    Traces.parent_span_id,
                    Traces.events_attributes,
                    Traces.span_attributes,
                )
                .filter(Traces.parent_span_id == '')
                .subquery()
            )

            stmt = (
                select(
                    func.min(inner_stmt.c.timestamp).cast(String).label('created_at'),
                    func.max(inner_stmt.c.timestamp)
                    .cast(String)
                    .label('latest_trace_ts'),
                    literal_column(
                        "SpanAttributes['traceloop.association.properties.session_uuid']"
                    ).label('session_uuid'),
                    func.count(inner_stmt.c.trace_id).label('traces'),
                    func.sum(inner_stmt.c.duration).label('durations'),
                    func.sum(func.length(inner_stmt.c.events_attributes) > 0).label(
                        'number_of_errors'
                    ),
                )
                .filter(
                    text(
                        "mapContains(SpanAttributes, 'traceloop.association.properties.session_uuid')"
                    )
                )
                .group_by(text('session_uuid'))
                .subquery()
            )
            return session.query(stmt).all()

    def get_trace_by_uuid(self, trace_id: str):
        with self.db.begin_session() as session:
            return session.query(Traces).where(Traces.trace_id == trace_id).all()
