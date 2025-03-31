from datetime import datetime
import logging
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query
from fastapi_pagination import Page, Params
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from app.core import get_config
from app.models.commons.order_type import OrderType
from app.models.exceptions import TimestampsRangeError
from app.models.traces.tracing_dto import SessionDTO, SpanDTO, TraceDTO
from app.models.traces.widget_dto import (
    LatenciesWidgetDTO,
    SessionsTracesDTO,
    TraceTimeseriesDTO,
)
from app.services.trace_service import TraceService

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceRoute:
    @staticmethod
    def get_router(trace_service: TraceService) -> APIRouter:
        router = APIRouter(tags=['trace_api'])

        @router.get(
            '/project/{project_uuid}/session/all',
            status_code=200,
            response_model=list[SessionDTO],
        )
        def get_all_session(project_uuid: UUID):
            return trace_service.get_all_sessions(
                project_uuid=project_uuid,
            )

        @router.get(
            '/project/{project_uuid}/session',
            status_code=200,
            response_model=Page[SessionDTO],
        )
        def get_all_session_paginated(
            project_uuid: UUID,
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return trace_service.get_all_sessions_paginated(
                project_uuid=project_uuid, params=params, order=_order, sort=_sort
            )

        @router.get(
            '/project/{project_uuid}/trace/all',
            status_code=200,
            response_model=list[TraceDTO],
        )
        def get_root_traces_by_project_uuid(
            project_uuid: UUID,
            trace_id: Annotated[Optional[str], Query(alias='traceId')] = None,
            session_uuid: Annotated[Optional[str], Query(alias='sessionUuid')] = None,
            from_timestamp: Annotated[
                Optional[int], Query(alias='fromTimestamp')
            ] = None,
            to_timestamp: Annotated[Optional[int], Query(alias='toTimestamp')] = None,
        ):
            if from_timestamp and to_timestamp:
                if from_timestamp > to_timestamp:
                    raise TimestampsRangeError(
                        message='to_timestamp must be greater than or equal to from_timestamp'
                    )
            return trace_service.get_all_root_traces_by_project_uuid(
                project_uuid=project_uuid,
                trace_id=trace_id,
                session_uuid=session_uuid,
                from_timestamp=datetime.fromtimestamp(from_timestamp)
                if from_timestamp
                else None,
                to_timestamp=datetime.fromtimestamp(to_timestamp)
                if to_timestamp
                else None,
            )

        @router.get(
            '/project/{project_uuid}/trace',
            status_code=200,
            response_model=Page[TraceDTO],
        )
        def get_root_traces_by_project_uuid_paginated(
            project_uuid: UUID,
            trace_id: Annotated[Optional[str], Query(alias='traceId')] = None,
            session_uuid: Annotated[Optional[str], Query(alias='sessionUuid')] = None,
            from_timestamp: Annotated[
                Optional[int], Query(alias='fromTimestamp')
            ] = None,
            to_timestamp: Annotated[Optional[int], Query(alias='toTimestamp')] = None,
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            if from_timestamp and to_timestamp:
                if from_timestamp > to_timestamp:
                    raise TimestampsRangeError(
                        message='to_timestamp must be greater than or equal to from_timestamp'
                    )

            params = Params(page=_page, size=_limit)
            return trace_service.get_all_root_traces_by_project_uuid_paginated(
                project_uuid=project_uuid,
                trace_id=trace_id,
                session_uuid=session_uuid,
                from_timestamp=datetime.fromtimestamp(from_timestamp)
                if from_timestamp
                else None,
                to_timestamp=datetime.fromtimestamp(to_timestamp)
                if to_timestamp
                else None,
                params=params,
                order=_order,
                sort=_sort,
            )

        @router.get(
            '/project/{project_uuid}/trace/{trace_id}',
            status_code=200,
            response_model=Optional[TraceDTO],
        )
        def get_trace_by_project_uuid_trace_id(
            project_uuid: UUID,
            trace_id: str,
        ):
            return trace_service.get_trace_by_project_uuid_trace_id(
                project_uuid=project_uuid,
                trace_id=trace_id,
            )

        @router.get(
            '/project/{project_uuid}/trace/{trace_id}/span/{span_id}',
            status_code=200,
            response_model=SpanDTO,
        )
        def get_span_by_id(project_uuid: UUID, trace_id: str, span_id: str):
            return trace_service.get_span_by_id(project_uuid, trace_id, span_id)

        @router.delete('/project/{project_uuid}/trace/{trace_id}', status_code=204)
        def delete_traces_by_project_uuid_trace_id(
            project_uuid: UUID,
            trace_id: str,
        ):
            return trace_service.delete_traces_by_project_uuid_trace_id(
                project_uuid=project_uuid,
                trace_id=trace_id,
            )

        @router.delete(
            '/project/{project_uuid}/session/{session_uuid}', status_code=204
        )
        def delete_traces_by_project_uuid_session_uuid(
            project_uuid: UUID,
            session_uuid: UUID,
        ):
            return trace_service.delete_traces_by_project_uuid_session_uuid(
                project_uuid=project_uuid,
                session_uuid=session_uuid,
            )

        @router.get(
            '/dashboard/project/{project_uuid}/root_latencies',
            status_code=200,
            response_model=LatenciesWidgetDTO,
        )
        def get_latencies_quantiles_for_root_traces_dashboard(
            project_uuid: UUID,
            from_timestamp: Annotated[int, Query(alias='fromTimestamp')],
            to_timestamp: Annotated[int, Query(alias='toTimestamp')],
        ):
            dashboard_result = (
                trace_service.get_latencies_quantiles_for_root_traces_dashboard(
                    project_uuid=project_uuid,
                    from_timestamp=datetime.fromtimestamp(from_timestamp),
                    to_timestamp=datetime.fromtimestamp(to_timestamp),
                )
            )
            if not dashboard_result:
                return Response(status_code=HTTP_204_NO_CONTENT)
            return dashboard_result

        @router.get(
            '/dashboard/project/{project_uuid}/root_latencies_session',
            status_code=200,
            response_model=List[LatenciesWidgetDTO],
        )
        def get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
            project_uuid: UUID,
            from_timestamp: Annotated[int, Query(alias='fromTimestamp')],
            to_timestamp: Annotated[int, Query(alias='toTimestamp')],
        ):
            dashboard_result = trace_service.get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
                project_uuid=project_uuid,
                from_timestamp=datetime.fromtimestamp(from_timestamp),
                to_timestamp=datetime.fromtimestamp(to_timestamp),
            )

            if not dashboard_result:
                return Response(status_code=HTTP_204_NO_CONTENT)
            return dashboard_result

        @router.get(
            '/dashboard/project/{project_uuid}/leaf_latencies',
            status_code=200,
            response_model=List[LatenciesWidgetDTO],
        )
        def get_latencies_quantiles_for_span_leaf_dashboard(
            project_uuid: UUID,
            from_timestamp: Annotated[int, Query(alias='fromTimestamp')],
            to_timestamp: Annotated[int, Query(alias='toTimestamp')],
        ):
            dashboard_result = (
                trace_service.get_latencies_quantiles_for_span_leaf_dashboard(
                    project_uuid=project_uuid,
                    from_timestamp=datetime.fromtimestamp(from_timestamp),
                    to_timestamp=datetime.fromtimestamp(to_timestamp),
                )
            )

            if not dashboard_result:
                return Response(status_code=HTTP_204_NO_CONTENT)
            return dashboard_result

        @router.get(
            '/dashboard/project/{project_uuid}/trace_by_time',
            status_code=200,
            response_model=TraceTimeseriesDTO,
        )
        def get_traces_by_time_dashboard(
            project_uuid: UUID,
            from_timestamp: Annotated[int, Query(alias='fromTimestamp')],
            to_timestamp: Annotated[int, Query(alias='toTimestamp')],
        ):
            if from_timestamp > to_timestamp:
                raise TimestampsRangeError(
                    message='to_timestamp must be greater than or equal to from_timestamp'
                )
            dashboard_result = trace_service.get_traces_by_time_dashboard(
                project_uuid,
                datetime.fromtimestamp(from_timestamp),
                datetime.fromtimestamp(to_timestamp),
                15,  # FIXME this should be proportional
            )

            if not dashboard_result:
                return Response(status_code=HTTP_204_NO_CONTENT)
            return dashboard_result

        @router.get(
            '/dashboard/project/{project_uuid}/traces-by-session',
            status_code=200,
            response_model=SessionsTracesDTO,
        )
        def get_sessions_traces_dashboard(
            project_uuid: UUID,
            from_timestamp: Annotated[int, Query(alias='fromTimestamp')],
            to_timestamp: Annotated[int, Query(alias='toTimestamp')],
        ):
            dashboard_result = trace_service.get_session_traces_dashboard(
                project_uuid=project_uuid,
                from_datetime=datetime.fromtimestamp(from_timestamp),
                to_datetime=datetime.fromtimestamp(to_timestamp),
            )

            if not dashboard_result:
                return Response(status_code=HTTP_204_NO_CONTENT)
            return dashboard_result

        return router
