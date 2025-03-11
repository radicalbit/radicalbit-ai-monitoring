from sqlalchemy import func, literal_column, select, text

from app.db.database import Database
from app.db.tables.traces_table import Traces


class TracesDAO:
    def __init__(self, database: Database):
        self.db = database

    def get_all_sessions(self):
        with self.db.begin_session() as session:
            stmt = (
                select(
                    literal_column(
                        "SpanAttributes['traceloop.association.properties.session_uuid']"
                    ).label('session_uuid'),
                    func.count(Traces.trace_id),
                    func.sum(Traces.duration),
                    func.sum(func.length(Traces.events_attributes) > 0),
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
