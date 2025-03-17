from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.project_dao import ProjectDAO
from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.exceptions import ProjectNotFoundError, TraceNotFoundError
from app.models.traces.tracing_dto import SessionDTO, SpanDTO, TraceDTO


class TraceService:
    def __init__(
        self,
        trace_dao: TraceDAO,
        project_dao: ProjectDAO,
    ):
        self.trace_dao = trace_dao
        self.project_dao = project_dao

    def get_all_sessions(
        self,
        project_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[SessionDTO]:
        self._check_project(project_uuid)
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
        self._check_project(project_uuid)
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

    def get_trace_by_project_uuid_trace_id(
        self,
        project_uuid: UUID,
        trace_id: str,
    ) -> Optional[TraceDTO]:
        self._check_project(project_uuid)
        traces = self.trace_dao.get_trace_by_project_uuid_trace_id(
            project_uuid, trace_id
        )
        list_of_traces = [dict(trace) for trace in traces.mappings()]
        if not list_of_traces:
            raise TraceNotFoundError(
                f'Trace with id {trace_id} not found in project {project_uuid}'
            )

        return TraceDTO.convert_traces_to_dto(list_of_traces, project_uuid)

    def get_span_by_id(
        self, project_uuid: UUID, trace_id: str, span_id: str
    ) -> SpanDTO:
        self._check_project(project_uuid)
        row = self.trace_dao.get_span_by_id(project_uuid, trace_id, span_id)
        if not row:
            raise TraceNotFoundError(
                f'Span {span_id} with project {project_uuid} and trace {trace_id} not found'
            )
        return SpanDTO.from_row_span(row)

    def _check_project(self, project_uuid: UUID):
        project = self.project_dao.get_by_uuid(project_uuid)
        if not project:
            raise ProjectNotFoundError(f'Project {project_uuid} not found')
