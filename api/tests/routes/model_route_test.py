import unittest
from unittest.mock import MagicMock
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.alert_dto import AlertDTO, AnomalyType
from app.models.commons.order_type import OrderType
from app.models.exceptions import (
    ErrorOut,
    ModelError,
    ModelInternalError,
    ModelNotFoundError,
    model_exception_handler,
)
from app.models.metrics.tot_percentages_dto import TotPercentagesDTO
from app.models.model_dto import ModelOut
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

        cls.client = TestClient(app, raise_server_exceptions=False)

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

    def test_update_model_ok(self):
        model_features = db_mock.get_sample_model_features()
        self.model_service.update_model_features_by_uuid = MagicMock(return_value=True)

        res = self.client.patch(
            f'{self.prefix}/{db_mock.MODEL_UUID}/update-features',
            json=jsonable_encoder(model_features),
        )

        assert res.status_code == 200
        self.model_service.update_model_features_by_uuid.assert_called_once_with(
            db_mock.MODEL_UUID, model_features
        )

    def test_update_model_ko(self):
        model_features = db_mock.get_sample_model_features()
        self.model_service.update_model_features_by_uuid = MagicMock(return_value=False)

        res = self.client.patch(
            f'{self.prefix}/{db_mock.MODEL_UUID}/update-features',
            json=jsonable_encoder(model_features),
        )

        assert res.status_code == 404
        self.model_service.update_model_features_by_uuid.assert_called_once_with(
            db_mock.MODEL_UUID, model_features
        )

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

    def test_get_all_models_paginated(self):
        model1 = db_mock.get_sample_model(id=1, uuid=uuid.uuid4(), name='model1')
        model2 = db_mock.get_sample_model(id=2, uuid=uuid.uuid4(), name='model2')
        model3 = db_mock.get_sample_model(id=3, uuid=uuid.uuid4(), name='model3')
        current1 = db_mock.get_sample_current_dataset(
            uuid=uuid.uuid4(), model_uuid=model1.uuid
        )
        current2 = db_mock.get_sample_current_dataset(
            uuid=uuid.uuid4(), model_uuid=model2.uuid
        )
        current3 = db_mock.get_sample_current_dataset(
            uuid=uuid.uuid4(), model_uuid=model3.uuid
        )
        metrics1 = db_mock.get_sample_current_metrics(current_uuid=current1.uuid)
        metrics2 = db_mock.get_sample_current_metrics(current_uuid=current2.uuid)
        metrics3 = db_mock.get_sample_current_metrics(current_uuid=current3.uuid)
        sample_models_out = [
            ModelOut.from_model(model1, percentages=metrics1.percentages),
            ModelOut.from_model(model2, percentages=metrics2.percentages),
            ModelOut.from_model(model3, percentages=metrics3.percentages),
        ]
        page = Page.create(
            items=sample_models_out, total=len(sample_models_out), params=Params()
        )
        self.model_service.get_all_models_paginated = MagicMock(return_value=page)

        res = self.client.get(f'{self.prefix}')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.model_service.get_all_models_paginated.assert_called_once_with(
            params=Params(page=1, size=50), order=OrderType.ASC, sort=None
        )

    def test_get_last_n_models(self):
        model0 = db_mock.get_sample_model()
        current0 = db_mock.get_sample_current_dataset()
        metrics0 = db_mock.get_sample_current_metrics(current_uuid=current0.uuid)
        model1_uuid = uuid.uuid4()
        model1 = db_mock.get_sample_model(id=2, uuid=model1_uuid, name='first_model')
        current1_uuid = uuid.uuid4()
        current1 = db_mock.get_sample_current_dataset(
            uuid=current1_uuid, model_uuid=model1_uuid
        )
        metrics1 = db_mock.get_sample_current_metrics(current_uuid=current1.uuid)

        sample_models_out = [
            ModelOut.from_model(model0, percentages=metrics0.percentages),
            ModelOut.from_model(model1, percentages=metrics1.percentages),
        ]

        self.model_service.get_last_n_models_percentages = MagicMock(
            return_value=sample_models_out
        )

        res = self.client.get(f'{self.prefix}/last_n', params={'n_models': 2})
        assert res.status_code == 200
        assert jsonable_encoder(sample_models_out) == res.json()
        self.model_service.get_last_n_models_percentages.assert_called_once_with(2)

    def test_get_last_n_alerts(self):
        model0 = db_mock.get_sample_model()
        current0 = db_mock.get_sample_current_dataset()
        model1_uuid = uuid.uuid4()
        model1 = db_mock.get_sample_model(id=2, uuid=model1_uuid, name='first_model')
        current1_uuid = uuid.uuid4()
        current1 = db_mock.get_sample_current_dataset(
            uuid=current1_uuid, model_uuid=model1_uuid
        )

        sample_alerts_out = [
            AlertDTO(
                model_name=model1.name,
                model_uuid=model1.uuid,
                reference_uuid=None,
                current_uuid=current1.uuid,
                completion_uuid=None,
                anomaly_type=AnomalyType.DRIFT,
                anomaly_features=['num1', 'num2'],
            ),
            AlertDTO(
                model_name=model0.name,
                model_uuid=model0.uuid,
                reference_uuid=None,
                current_uuid=current0.uuid,
                completion_uuid=None,
                anomaly_type=AnomalyType.DRIFT,
                anomaly_features=['num1', 'num2'],
            ),
        ]

        self.model_service.get_last_n_alerts = MagicMock(return_value=sample_alerts_out)

        res = self.client.get(f'{self.prefix}/last_n_alerts', params={'n_alerts': 2})
        assert res.status_code == 200
        assert jsonable_encoder(sample_alerts_out) == res.json()
        self.model_service.get_last_n_alerts.assert_called_once_with(2)

    def test_get_tot_percentages(self):
        sample_tot_percs_out = TotPercentagesDTO.from_dict(
            {'data_quality': 1.0, 'model_quality': -1, 'drift': 0.5}
        )

        self.model_service.get_summarized_percentages = MagicMock(
            return_value=sample_tot_percs_out
        )

        res = self.client.get(f'{self.prefix}/tot_percentages')
        assert res.status_code == 200
        assert jsonable_encoder(sample_tot_percs_out) == res.json()
        self.model_service.get_summarized_percentages.assert_called_once()

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
