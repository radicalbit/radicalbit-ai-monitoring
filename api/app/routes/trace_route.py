import logging
from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.core import get_config
from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO
from app.services.trace_service import TraceService

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceRoute:
    @staticmethod
    def get_router(trace_service: TraceService) -> APIRouter:
        router = APIRouter(tags=['trace_api'])

        @router.get('/session/all', status_code=200, response_model=Page[SessionDTO])
        def get_all_session_paginated(
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return trace_service.get_all_sessions(
                params=params, order=_order, sort=_sort
            )

        return router
