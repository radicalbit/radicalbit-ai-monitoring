import datetime
import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.core import get_config
from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO, TraceDTO
from app.services.trace_service import TraceService

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceRoute:
    @staticmethod
    def get_router(trace_service: TraceService) -> APIRouter:
        router = APIRouter(tags=['trace_api'])

        @router.get(
            '/session/all/{project_uuid}',
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
            return trace_service.get_all_sessions(
                project_uuid=project_uuid, params=params, order=_order, sort=_sort
            )

        @router.get(
            '/project/{project_uuid}', status_code=200, response_model=Page[TraceDTO]
        )
        def get_root_traces_by_project_uuid(
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
            params = Params(page=_page, size=_limit)
            return trace_service.get_all_root_traces_by_project_uuid(
                project_uuid=project_uuid,
                trace_id=trace_id,
                session_uuid=session_uuid,
                from_timestamp=datetime.datetime.fromtimestamp(from_timestamp)
                if from_timestamp
                else None,
                to_timestamp=datetime.datetime.fromtimestamp(to_timestamp)
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

        return router
