import logging
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import Response

from app.core import get_config
from app.models.exceptions import OtelUnauthorizedError
from app.services.otel_service import OtelService

logger = logging.getLogger(get_config().log_config.logger_name)


class OtelRoute:
    @staticmethod
    def get_router(otel_service: OtelService) -> APIRouter:
        router = APIRouter(tags=['otel_api'])

        def _get_api_key_from_token(token: Optional[str]):
            if not token:
                logger.error('Missing Authorization token')
                raise OtelUnauthorizedError('Missing Authorization token')
            if not token.startswith('Bearer '):
                logger.error('The token must be a Bearer')
                raise OtelUnauthorizedError('The token must be a Bearer')
            return token.removeprefix('Bearer ').strip()

        @router.post(
            '/v1/traces',
            status_code=201,
        )
        async def write_traces(request: Request) -> Response:
            token = request.headers.get('Authorization')
            api_key = _get_api_key_from_token(token)
            body = await request.body()
            headers = dict(request.headers)

            response = await otel_service.write_traces(api_key, body, headers)

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get('content-type', 'application/json'),
            )

        @router.post(
            '/v1/metrics',
            status_code=201,
        )
        async def write_metrics(request: Request) -> Response:
            token = request.headers.get('Authorization')
            api_key = _get_api_key_from_token(token)
            body = await request.body()
            headers = dict(request.headers)

            response = await otel_service.write_metrics(api_key, body, headers)

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.headers.get('content-type', 'application/json'),
            )

        return router
