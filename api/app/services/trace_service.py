from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO


class TraceService:
    def __init__(
        self,
        trace_dao: TraceDAO,
    ):
        self.trace_dao = trace_dao

    def get_all_sessions(
        self,
        project_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[SessionDTO]:
        sessions = self.trace_dao.get_all_sessions(
            project_uuid=project_uuid, params=params, order=order, sort=sort
        )
        sessions_dto = [SessionDTO.model_validate(s) for s in sessions.items]
        return Page.create(
            items=sessions_dto,
            params=params,
            total=sessions.total,
        )
