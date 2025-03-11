from app.db.database import Database
from app.db.tables.traces_table import Traces


class TracesDAO:
    def __init__(self, database: Database):
        self.db = database

    def get_all_sessions(self):
        pass

    def get_trace_by_uuid(self, trace_id: str):
        with self.db.begin_session() as session:
            return session.query(Traces).where(Traces.trace_id == trace_id).all()
