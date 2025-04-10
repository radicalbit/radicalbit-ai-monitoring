import unittest
from unittest.mock import ANY, AsyncMock, MagicMock

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from httpx import Response
from starlette.testclient import TestClient

from app.models.exceptions import OtelError, otel_exception_handler
from app.routes.otel_route import OtelRoute
from app.services.otel_service import OtelService


class OtelRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.otel_service = MagicMock(spec_set=OtelService)
        cls.prefix = '/api/otel'

        router = OtelRoute.get_router(cls.otel_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.add_exception_handler(OtelError, otel_exception_handler)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app, raise_server_exceptions=False)

    def test_write_traces_ok(self):
        mock_response = Response(
            status_code=201,
            content=b'ok',
            headers={'content-type': 'application/json'},
        )
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        self.otel_service.write_traces = AsyncMock(return_value=mock_response)

        res = self.client.post(
            f'{self.prefix}/v1/traces',
            json=jsonable_encoder('trace-data'),
            headers=headers,
        )
        assert res.status_code == 201
        assert res.content == b'ok'
        self.otel_service.write_traces.assert_awaited_once_with(
            api_key, b'"trace-data"', ANY
        )

    def test_write_metrics_ok(self):
        mock_response = Response(
            status_code=201,
            content=b'ok',
            headers={'content-type': 'application/json'},
        )
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        self.otel_service.write_metrics = AsyncMock(return_value=mock_response)

        res = self.client.post(
            f'{self.prefix}/v1/metrics',
            json=jsonable_encoder('metrics-data'),
            headers=headers,
        )
        assert res.status_code == 201
        assert res.content == b'ok'
        self.otel_service.write_metrics.assert_awaited_once_with(
            api_key, b'"metrics-data"', ANY
        )

    def test_exception_handler_unauthorized_error_missing_token(self):
        res = self.client.post(
            f'{self.prefix}/v1/traces',
            json=jsonable_encoder('trace-data'),
        )
        assert res.status_code == 401
        assert res.json() == {'message': 'Missing Authorization token'}
        self.otel_service.write_traces.assert_not_called()

    def test_exception_handler_unauthorized_error_invalid_token(self):
        headers = {'Authorization': 'InvalidToken xyz'}

        res = self.client.post(
            f'{self.prefix}/v1/traces',
            json=jsonable_encoder('trace-data'),
            headers=headers,
        )

        assert res.status_code == 401
        assert res.json() == {'message': 'The token must be a Bearer'}
        self.otel_service.write_traces.assert_not_called()
