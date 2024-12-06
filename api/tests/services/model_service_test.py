import unittest
from unittest.mock import MagicMock
import uuid

from fastapi_pagination import Page, Params
import pytest

from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.models.alert_dto import AnomalyType
from app.models.exceptions import ModelError, ModelNotFoundError
from app.models.model_dto import ModelOut, ModelType
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
        cls.current_metrics_dao: CurrentDatasetMetricsDAO = MagicMock(
            spec_set=CurrentDatasetMetricsDAO
        )
        cls.mocks = [cls.model_dao, cls.rd_dao, cls.cd_dao]

    def test_create_model_ok(self):
        model = db_mock.get_sample_model()
        self.model_dao.insert = MagicMock(return_value=model)
        model_in = db_mock.get_sample_model_in()
        res = self.model_service.create_model(model_in)
        self.model_dao.insert.assert_called_once()

        assert res == ModelOut.from_model(model)

    def test_create_text_generation_model_ok(self):
        model = db_mock.get_sample_model(
            model_type=ModelType.TEXT_GENERATION,
            features=None,
            target=None,
            outputs=None,
            timestamp=None,
        )
        self.model_dao.insert = MagicMock(return_value=model)
        model_in = db_mock.get_sample_model_in(
            model_type=ModelType.TEXT_GENERATION,
            features=None,
            target=None,
            outputs=None,
            timestamp=None,
        )
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
            latest_reference_dataset=reference_dataset,
            latest_current_dataset=current_dataset,
        )

    def test_get_model_by_uuid_not_found(self):
        self.model_dao.get_by_uuid = MagicMock(return_value=None)
        pytest.raises(
            ModelNotFoundError, self.model_service.get_model_by_uuid, model_uuid
        )
        self.model_dao.get_by_uuid.assert_called_once()

    def test_update_model_ok(self):
        model_features = db_mock.get_sample_model_features()
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        self.model_dao.update_features = MagicMock(return_value=1)
        res = self.model_service.update_model_features_by_uuid(
            model_uuid, model_features
        )
        feature_dict = [feature.to_dict() for feature in model_features.features]
        self.rd_dao.get_latest_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.model_dao.update_features.assert_called_once_with(model_uuid, feature_dict)

        assert res is True

    def test_update_model_ko(self):
        model_features = db_mock.get_sample_model_features()
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        self.model_dao.update_features = MagicMock(return_value=0)
        res = self.model_service.update_model_features_by_uuid(
            model_uuid, model_features
        )
        feature_dict = [feature.to_dict() for feature in model_features.features]
        self.rd_dao.get_latest_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.model_dao.update_features.assert_called_once_with(model_uuid, feature_dict)

        assert res is False

    def test_update_model_freezed(self):
        model_features = db_mock.get_sample_model_features()
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=db_mock.get_sample_reference_dataset()
        )
        self.model_dao.update_features = MagicMock(return_value=0)
        with pytest.raises(ModelError):
            self.model_service.update_model_features_by_uuid(model_uuid, model_features)
            feature_dict = [feature.to_dict() for feature in model_features.features]
            self.rd_dao.get_latest_reference_dataset_by_model_uuid.assert_called_once_with(
                model_uuid
            )
            self.model_dao.update_features.assert_called_once_with(
                model_uuid, feature_dict
            )

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
        current1 = db_mock.get_sample_current_dataset(
            uuid=uuid.uuid4(), model_uuid=model1.uuid
        )
        current2 = db_mock.get_sample_current_dataset(
            uuid=uuid.uuid4(), model_uuid=model2.uuid
        )
        metrics1 = db_mock.get_sample_current_metrics(current_uuid=current1.uuid)
        metrics2 = db_mock.get_sample_current_metrics(current_uuid=current2.uuid)
        sample_models = [(model1, metrics1), (model2, metrics2), (model3, None)]
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
        assert result.items[0].percentages is not None
        assert result.items[1].percentages is not None
        assert result.items[2].percentages is None

    def test_get_all_models_ok(self):
        model1 = db_mock.get_sample_model(id=1, uuid=uuid.uuid4(), name='model1')
        model2 = db_mock.get_sample_model(id=2, uuid=uuid.uuid4(), name='model2')
        model3 = db_mock.get_sample_model(id=3, uuid=uuid.uuid4(), name='model3')
        sample_models = [model1, model2, model3]
        self.model_dao.get_all = MagicMock(return_value=sample_models)
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        self.cd_dao.get_latest_current_dataset_by_model_uuid = MagicMock(
            return_value=None
        )

        result = self.model_service.get_all_models()

        self.model_dao.get_all.assert_called_once()

        assert len(result) == 3
        assert result[0].name == 'model1'
        assert result[1].name == 'model2'
        assert result[2].name == 'model3'

    def test_get_last_n_models_percentages(self):
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

        sample = [(model1, metrics1), (model0, metrics0)]

        self.model_dao.get_last_n_percentages = MagicMock(return_value=sample)
        self.rd_dao.get_latest_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        self.cd_dao.get_latest_current_dataset_by_model_uuid = MagicMock(
            return_value=None
        )

        result = self.model_service.get_last_n_models_percentages(2)
        assert result[0].name == model1.name
        assert result[1].name == model0.name
        assert result[1].updated_at < result[0].updated_at

    def test_get_summarized_percentages(self):
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

        sample = [(model1, metrics1), (model0, metrics0)]

        self.model_dao.get_last_n_percentages = MagicMock(return_value=sample)

        result = self.model_service.get_summarized_percentages()
        assert result.data_quality == 1.0
        assert result.model_quality == -1

    def test_get_last_n_alerts(self):
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

        sample = [(model1, metrics1), (model0, metrics0)]

        self.model_dao.get_last_n_percentages = MagicMock(return_value=sample)

        result = self.model_service.get_last_n_alerts(2)

        assert result[0].model_uuid == model1.uuid
        assert result[0].anomaly_type == AnomalyType.DRIFT
        assert result[1].anomaly_features == ['num1', 'num2']


model_uuid = db_mock.MODEL_UUID
