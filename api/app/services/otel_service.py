import logging

from httpx import AsyncClient, RequestError, Response
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
)

from app.core import get_config
from app.db.dao.api_key_dao import ApiKeyDAO
from app.models.exceptions import OtelInternalError, OtelUnauthorizedError
from app.services.commons.keyed_hash_algorithm import hash_key

logger = logging.getLogger(get_config().log_config.logger_name)


class OtelService:
    def __init__(
        self,
        api_key_dao: ApiKeyDAO,
    ):
        self.api_key_dao = api_key_dao

    async def write_traces(self, api_key: str, body: bytes, headers: dict) -> Response:
        hashed_key = hash_key(api_key)
        retrieved = self.api_key_dao.get_by_hashed_key(hashed_key)

        if not retrieved:
            raise OtelUnauthorizedError('Api Key not found')

        body_with_project = self._inject_project_uuid(body, str(retrieved.project_uuid))
        return await self._forward_to_collector(body_with_project, headers, 'traces')

    async def write_metrics(self, api_key: str, body: bytes, headers: dict) -> Response:
        hashed_key = hash_key(api_key)
        retrieved = self.api_key_dao.get_by_hashed_key(hashed_key)

        if not retrieved:
            raise OtelUnauthorizedError('Api Key not found')

        body_with_project = self._inject_project_uuid(body, str(retrieved.project_uuid))
        return await self._forward_to_collector(body_with_project, headers, 'metrics')

    @staticmethod
    def _inject_project_uuid(body: bytes, project_uuid: str) -> bytes:
        try:
            parsed = ExportTraceServiceRequest()
            parsed.ParseFromString(body)

            for resource_span in parsed.resource_spans:
                resource = resource_span.resource
                for attribute in resource.attributes:
                    if attribute.key == 'service.name':
                        attribute.value.string_value = project_uuid

            return parsed.SerializeToString()
        except Exception as e:
            logger.warning('Failed to inject project_uuid into trace: %s', e)
            return body

    @staticmethod
    async def _forward_to_collector(
        body: bytes, headers: dict, suffix_route: str
    ) -> Response:
        headers = headers.copy()
        headers.pop('content-length', None)
        headers['content-length'] = str(len(body))

        async with AsyncClient() as client:
            try:
                return await client.post(
                    url=f'http://otel-collector:4318/v1/{suffix_route}',
                    content=body,
                    headers=headers,
                )
            except RequestError as e:
                logger.error('Failed to forward request to collector: %s', e)
                raise OtelInternalError('Failed to forward request to collector') from e
