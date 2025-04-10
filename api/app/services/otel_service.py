import logging

from httpx import AsyncClient, RequestError, Response

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
        if retrieved:
            return await self._forward_to_collector(body, headers, 'traces')

        raise OtelUnauthorizedError('Api Key not found')

    async def write_metrics(self, api_key: str, body: bytes, headers: dict) -> Response:
        hashed_key = hash_key(api_key)
        retrieved = self.api_key_dao.get_by_hashed_key(hashed_key)
        if retrieved:
            return await self._forward_to_collector(body, headers, 'metrics')

        raise OtelUnauthorizedError('Api Key not found')

    @staticmethod
    async def _forward_to_collector(
        body: bytes, headers: dict, suffix_route: str
    ) -> Response:
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
