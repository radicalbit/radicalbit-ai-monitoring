import unittest
from unittest.mock import MagicMock
import uuid

from fastapi_pagination import Page, Params
import pytest

from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.models.exceptions import ModelNotFoundError
from app.models.model_dto import ModelOut
from app.models.model_order import OrderType
from app.services.model_service import ModelService
from tests.commons import db_mock


class ModelServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model_dao: ModelDAO = MagicMock(spec_set=ModelDAO)
        cls.rd_dao: ReferenceDatasetDAO = MagicMock(spec_set=ReferenceDatasetDAO)
        cls.cd_dao: CurrentDatasetDAO = MagicMock(spec_set=CurrentDatasetDAO)
        cls.model_service = ModelService(
            model_dao=cls.model_dao,
            reference_dataset_dao=cls.rd_dao,
            current_dataset_dao=cls.cd_dao,
        )
        cls.mocks = [cls.model_dao, cls.rd_dao, cls.cd_dao]

    def test_create_model_ok(self):
        model = db_mock.get_sample_model()
        self.model_dao.insert = MagicMock(return_value=model)
        model_in = db_mock.get_sample_model_in()
        res = self.model_service.create_model(model_in)
        self.model_dao.insert.assert_called_once()

        assert res == ModelOut.from_model(model)

    def test_get_model_by_uuid_ok(self):
        model = db_mock.get_sample_model()
        reference_dataset = db_mock.get_sample_reference_dataset(model_uuid=model.uuid)
        current_dataset = db_mock.get_sample_current_dataset(model_uuid=model.uuid)
        self.model_dao.get_by_uuid = MagicMock(return_value=model)
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.cd_dao.get_latest_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        res = self.model_service.get_model_by_uuid(model_uuid)
        self.model_dao.get_by_uuid.assert_called_once()
        self.rd_dao.get_latest_reference_dataset_by_model_uuid.assert_called_once()
        self.cd_dao.get_latest_current_dataset_by_model_uuid.assert_called_once()

        assert res == ModelOut.from_model(
            model=model,
            latest_reference_uuid=reference_dataset.uuid,
            latest_current_uuid=current_dataset.uuid,
        )

    def test_get_model_by_uuid_not_found(self):
        self.model_dao.get_by_uuid = MagicMock(return_value=None)
        pytest.raises(
            ModelNotFoundError, self.model_service.get_model_by_uuid, model_uuid
        )
        self.model_dao.get_by_uuid.assert_called_once()

    def test_delete_model_ok(self):
        model = db_mock.get_sample_model()
        self.model_dao.get_by_uuid = MagicMock(return_value=model)
        res = self.model_service.delete_model(model_uuid)
        self.model_dao.get_by_uuid.assert_called_once_with(model.uuid)
        self.model_dao.delete.assert_called_once_with(model.uuid)

        assert res == ModelOut.from_model(model)

    def test_get_all_models_paginated_ok(self):
        model1 = db_mock.get_sample_model(id=1, uuid=uuid.uuid4(), name='model1')
        model2 = db_mock.get_sample_model(id=2, uuid=uuid.uuid4(), name='model2')
        model3 = db_mock.get_sample_model(id=3, uuid=uuid.uuid4(), name='model3')
        sample_models = [model1, model2, model3]
        page = Page.create(
            sample_models,
            total=len(sample_models),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )
        self.model_dao.get_all_paginated = MagicMock(return_value=page)
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        self.cd_dao.get_latest_current_dataset_by_model_uuid = MagicMock(
            return_value=None
        )

        result = self.model_service.get_all_models_paginated(
            params=Params(page=1, size=10), order=OrderType.ASC, sort=None
        )

        self.model_dao.get_all_paginated.assert_called_once_with(
            params=Params(page=1, size=10), order=OrderType.ASC, sort=None
        )

        assert result.total == 3
        assert len(result.items) == 3
        assert result.items[0].name == 'model1'
        assert result.items[1].name == 'model2'
        assert result.items[2].name == 'model3'


model_uuid = db_mock.MODEL_UUID
