import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient

from app.models.exceptions import ProjectError, project_exception_handler
from app.models.traces.api_key_dto import ApiKeyOut
from app.routes.api_key_route import ApiKeyRoute
from app.services.api_key_service import ApiKeyService
from tests.commons import db_mock


class ApiKeyRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_key_service = MagicMock(spec_set=ApiKeyService)
        cls.prefix = '/api/api-key'

        router = ApiKeyRoute.get_router(cls.api_key_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.add_exception_handler(ProjectError, project_exception_handler)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app, raise_server_exceptions=False)

    def test_create_api_key(self):
        api_key_in = db_mock.get_sample_api_key_in()
        api_key = db_mock.get_sample_api_key()
        api_key_out = ApiKeyOut.from_api_key(
            api_key=api_key, plain_api_key=db_mock.PLAIN_KEY
        )
        self.api_key_service.create_api_key = MagicMock(return_value=api_key_out)
        res = self.client.post(
            f'{self.prefix}/project/{db_mock.PROJECT_UUID}',
            json=jsonable_encoder(api_key_in),
        )
        assert res.status_code == 201
        assert jsonable_encoder(api_key_out) == res.json()
        self.api_key_service.create_api_key.assert_called_once_with(
            db_mock.PROJECT_UUID, api_key_in
        )
