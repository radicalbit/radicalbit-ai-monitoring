import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.commons.order_type import OrderType
from app.models.exceptions import (
    ApiKeyError,
    ApiKeyNotFoundError,
    ExistingApiKeyError,
    api_key_exception_handler,
)
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
        app.add_exception_handler(ApiKeyError, api_key_exception_handler)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app, raise_server_exceptions=False)

    def test_create_api_key(self):
        api_key_in = db_mock.get_sample_api_key_in()
        api_key = db_mock.get_sample_api_key()
        api_key_out = ApiKeyOut.from_api_key(
            api_key=api_key,
            plain_api_key=db_mock.PLAIN_KEY,
            project_uuid=db_mock.PROJECT_UUID,
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

    def test_create_api_existing_err(self):
        api_key_in = db_mock.get_sample_api_key_in()
        self.api_key_service.create_api_key = MagicMock()
        self.api_key_service.create_api_key.side_effect = ExistingApiKeyError(
            f'A key with name {api_key_in.name} already exists in project {db_mock.PROJECT_UUID}'
        )
        res = self.client.post(
            f'{self.prefix}/project/{db_mock.PROJECT_UUID}',
            json=jsonable_encoder(api_key_in),
        )
        assert res.status_code == 400

    def test_get_all(self):
        api_keys = [
            db_mock.get_sample_api_key(name='api_key'),
            db_mock.get_sample_api_key(name='api_key_one'),
            db_mock.get_sample_api_key(name='api_key_two'),
        ]
        api_keys = [
            ApiKeyOut.from_api_key_obscured(i, db_mock.PROJECT_UUID) for i in api_keys
        ]
        self.api_key_service.get_all = MagicMock(return_value=api_keys)
        res = self.client.get(f'{self.prefix}/project/{db_mock.PROJECT_UUID}/all')
        assert res.status_code == 200
        assert jsonable_encoder(api_keys) == res.json()
        self.api_key_service.get_all.assert_called_once_with(db_mock.PROJECT_UUID)

    def test_get_all_paginated(self):
        api_keys = [
            db_mock.get_sample_api_key(name='api_key'),
            db_mock.get_sample_api_key(name='api_key_one'),
            db_mock.get_sample_api_key(name='api_key_two'),
        ]
        api_keys = [
            ApiKeyOut.from_api_key_obscured(i, db_mock.PROJECT_UUID) for i in api_keys
        ]
        page = Page.create(items=api_keys, total=len(api_keys), params=Params())
        self.api_key_service.get_all_paginated = MagicMock(return_value=page)
        res = self.client.get(f'{self.prefix}/project/{db_mock.PROJECT_UUID}')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.api_key_service.get_all_paginated.assert_called_once_with(
            db_mock.PROJECT_UUID, Params(page=1, size=50), OrderType.ASC, None
        )

    def test_get_api_key(self):
        api_key = db_mock.get_sample_api_key(name='api_key')
        api_key_out = ApiKeyOut.from_api_key_obscured(api_key, db_mock.PROJECT_UUID)
        self.api_key_service.get_api_key = MagicMock(return_value=api_key_out)
        res = self.client.get(
            f'{self.prefix}/project/{db_mock.PROJECT_UUID}/api-keys/{api_key.name}'
        )
        assert res.status_code == 200
        assert jsonable_encoder(api_key_out) == res.json()
        self.api_key_service.get_api_key.assert_called_once_with(
            db_mock.PROJECT_UUID, 'api_key'
        )

    def test_get_api_key_not_found(self):
        self.api_key_service.get_api_key = MagicMock()
        self.api_key_service.get_api_key.side_effect = ApiKeyNotFoundError(
            'ApiKey fake not found'
        )
        res = self.client.get(
            f'{self.prefix}/project/{db_mock.PROJECT_UUID}/api-keys/fake'
        )
        assert res.status_code == 404
