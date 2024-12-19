import unittest
from unittest.mock import MagicMock

from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app import main
from app.models.model_dto import ModelOut, ModelType
from app.services.model_service import ModelService
from tests.commons import db_mock
from tests.commons.modelin_factory import get_model_sample_wrong


class TestValidationModelRoute(unittest.TestCase):
    def setUp(self):
        self.model_service = MagicMock(spec_set=ModelService)
        self.prefix = '/api/models'
        self.client = TestClient(main.app, raise_server_exceptions=False)

    def test_request_validation_exception_handler(self):
        modelin_data = get_model_sample_wrong(
            fail_fields=['timestamp'], model_type=ModelType.BINARY
        )
        model = db_mock.get_sample_model()
        model_out = ModelOut.from_model(model)
        self.model_service.create_model = MagicMock(return_value=model_out)

        response = self.client.post(
            f'{self.prefix}',
            json=jsonable_encoder(modelin_data),
        )

        assert response.status_code == 422
        assert response.json()['message'] == 'timestamp must be a datetime'

        self.model_service.create_model.assert_not_called()
