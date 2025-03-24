from datetime import datetime
import logging
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.core import get_config
from app.db.dao.project_dao import ProjectDAO
from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.exceptions import ProjectNotFoundError, TraceNotFoundError
from app.models.traces.tracing_dto import SessionDTO, SpanDTO, TraceDTO
from app.models.traces.widget_dto import LatenciesWidgetDTO, TraceTimeseriesDTO

logger = logging.getLogger(get_config().log_config.logger_name)


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

    def delete_traces_by_project_uuid_trace_id(
        self,
        project_uuid: UUID,
        trace_id: str,
    ) -> int:
        self._check_project(project_uuid)
        return self.trace_dao.delete_traces_by_project_uuid_trace_id(
            project_uuid, trace_id
        )

    def delete_traces_by_project_uuid_session_uuid(
        self,
        project_uuid: UUID,
        session_uuid: UUID,
    ) -> int:
        self._check_project(project_uuid)
        return self.trace_dao.delete_traces_by_project_uuid_session_uuid(
            project_uuid, session_uuid
        )

    def get_latencies_quantiles_for_root_traces_dashboard(
        self,
        project_uuid: UUID,
        from_timestamp: datetime,
        to_timestamp: datetime,
    ):
        self._check_project(project_uuid)
        latencies_quantiles = (
            self.trace_dao.get_latencies_quantiles_for_root_traces_dashboard(
                project_uuid, from_timestamp, to_timestamp
            )
        )
        if not latencies_quantiles:
            raise TraceNotFoundError(
                f'Latencies quantiles for root traces for {project_uuid} not found'
            )
        return LatenciesWidgetDTO.model_validate(latencies_quantiles)

    def get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
        self,
        project_uuid: UUID,
        from_timestamp: datetime,
        to_timestamp: datetime,
    ):
        self._check_project(project_uuid)
        latencies_quantiles = self.trace_dao.get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
            project_uuid, from_timestamp, to_timestamp
        )
        latencies_quantiles_dto = [
            LatenciesWidgetDTO.model_validate(project_and_session_latencies)
            for project_and_session_latencies in latencies_quantiles
        ]
        if not latencies_quantiles_dto:
            raise TraceNotFoundError(
                f'Latencies quantiles for root traces for {project_uuid} grouped by session_uuid not found'
            )
        return latencies_quantiles_dto

    def get_latencies_quantiles_for_span_leaf_dashboard(
        self,
        project_uuid: UUID,
        from_timestamp: datetime,
        to_timestamp: datetime,
    ):
        self._check_project(project_uuid)
        latencies_quantiles = (
            self.trace_dao.get_latencies_quantiles_for_span_leaf_dashboard(
                project_uuid, from_timestamp, to_timestamp
            )
        )
        latencies_quantiles_dto = [
            LatenciesWidgetDTO.model_validate(span_latencies)
            for span_latencies in latencies_quantiles
        ]
        if not latencies_quantiles_dto:
            raise TraceNotFoundError(
                f'Latencies quantiles for leaf span for {project_uuid} grouped by span_name not found'
            )
        return latencies_quantiles_dto

    def get_traces_by_time_dashboard(
        self,
        project_uuid: UUID,
        from_datetime: datetime,
        to_datetime: datetime,
        n: int,
    ) -> TraceTimeseriesDTO:
        self._check_project(project_uuid)
        interval_size_seconds = self._extract_interval(from_datetime, to_datetime, n)
        results = self.trace_dao.get_traces_by_time_dashboard(
            project_uuid, from_datetime, to_datetime, interval_size_seconds
        )
        return TraceTimeseriesDTO.from_raw(
            project_uuid=project_uuid,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            n=n,
            interval_size_seconds=interval_size_seconds,
            rows=results,
        )

    def _check_project(self, project_uuid: UUID):
        project = self.project_dao.get_by_uuid(project_uuid)
        if not project:
            raise ProjectNotFoundError(f'Project {project_uuid} not found')

    @staticmethod
    def _extract_interval(
        from_datetime: datetime, to_datetime: datetime, n: int
    ) -> int:
        time_diff_seconds = (to_datetime - from_datetime).total_seconds()
        return int(time_diff_seconds / n)
