from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO, TraceDTO


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
    ) -> Page[TraceDTO]:
        results = self.trace_dao.get_all_root_traces_by_project_uuid(
            project_uuid,
            trace_id,
            session_uuid,
            from_timestamp,
            to_timestamp,
            params,
            order,
            sort,
        )
        list_of_traces = [TraceDTO.model_validate(trace) for trace in results.items]

        return Page.create(items=list_of_traces, params=params, total=results.total)
