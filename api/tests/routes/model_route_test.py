import unittest
from unittest.mock import MagicMock
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.exceptions import (
    ErrorOut,
    ModelError,
    ModelInternalError,
    ModelNotFoundError,
    model_exception_handler,
)
from app.models.model_dto import ModelOut
from app.models.model_order import OrderType
from app.routes.model_route import ModelRoute
from app.services.model_service import ModelService
from tests.commons import db_mock


class ModelRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_service = MagicMock(spec_set=ModelService)
        cls.prefix = '/api/models'

        router = ModelRoute.get_router(cls.model_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.add_exception_handler(ModelError, model_exception_handler)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app)

    def test_create_model(self):
        model_in = db_mock.get_sample_model_in()
        model = db_mock.get_sample_model()
        model_out = ModelOut.from_model(model)
        self.model_service.create_model = MagicMock(return_value=model_out)

        res = self.client.post(
            f'{self.prefix}',
            json=jsonable_encoder(model_in),
        )

        assert res.status_code == 201
        assert jsonable_encoder(model_out) == res.json()
        self.model_service.create_model.assert_called_once_with(model_in)

    def test_get_model_by_uuid(self):
        model = db_mock.get_sample_model()
        model_out = ModelOut.from_model(model)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model_out)

        res = self.client.get(f'{self.prefix}/{model.uuid}')
        assert res.status_code == 200
        assert jsonable_encoder(model_out) == res.json()
        self.model_service.get_model_by_uuid.assert_called_once_with(model.uuid)

    def test_delete_model(self):
        model = db_mock.get_sample_model()
        model_out = ModelOut.from_model(model)
        self.model_service.delete_model = MagicMock(return_value=model_out)

        res = self.client.delete(f'{self.prefix}/{model.uuid}')
        assert res.status_code == 200
        assert jsonable_encoder(model_out) == res.json()
        self.model_service.delete_model.assert_called_once_with(model.uuid)

    def test_get_all_models(self):
        model1 = db_mock.get_sample_model(id=1, uuid=uuid.uuid4(), name='model1')
        model2 = db_mock.get_sample_model(id=2, uuid=uuid.uuid4(), name='model2')
        model3 = db_mock.get_sample_model(id=3, uuid=uuid.uuid4(), name='model3')

        sample_models_out = [
            ModelOut.from_model(model1),
            ModelOut.from_model(model2),
            ModelOut.from_model(model3),
        ]
        page = Page.create(
            items=sample_models_out, total=len(sample_models_out), params=Params()
        )
        self.model_service.get_all_models = MagicMock(return_value=page)

        res = self.client.get(f'{self.prefix}')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.model_service.get_all_models.assert_called_once_with(
            params=Params(page=1, size=50), order=OrderType.ASC, sort=None
        )

    def test_exception_handler_model_internal_error(self):
        model_in = db_mock.get_sample_model_in()
        self.model_service.create_model = MagicMock(
            side_effect=ModelInternalError('error')
        )

        res = self.client.post(
            f'{self.prefix}',
            json=jsonable_encoder(model_in),
        )

        assert res.status_code == 500
        assert jsonable_encoder(ErrorOut('error')) == res.json()
        self.model_service.create_model.assert_called_once_with(model_in)

    def test_exception_handler_model_not_found_error(self):
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(
            side_effect=ModelNotFoundError('error')
        )

        res = self.client.get(f'{self.prefix}/{model.uuid}')

        assert res.status_code == 404
        assert jsonable_encoder(ErrorOut('error')) == res.json()
        self.model_service.get_model_by_uuid.assert_called_once_with(model.uuid)
