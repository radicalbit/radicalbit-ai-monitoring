import logging

from fastapi import APIRouter

from app.core import get_config
from app.models.traces.tracing_dto import SessionDTO
from app.services.trace_service import TraceService

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceRoute:
    @staticmethod
    def get_router(trace_service: TraceService) -> APIRouter:
        router = APIRouter(tags=['trace_api'])

        @router.get('/all', status_code=200, response_model=list[SessionDTO])
        def get_project_by_uuid():
            return trace_service.get_all_sessions()

        return router
