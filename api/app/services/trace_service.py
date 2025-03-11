from app.db.dao.traces_dao import TraceDAO
from app.models.traces.tracing_dto import SessionDTO


class TraceService:
    def __init__(
        self,
        trace_dao: TraceDAO,
    ):
        self.trace_dao = trace_dao

    def get_all_sessions(self) -> list[SessionDTO]:
        return [SessionDTO.model_validate(s) for s in self.trace_dao.get_all_sessions()]
