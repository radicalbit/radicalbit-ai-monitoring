from typing import Dict, List
import uuid

from app.db.dao.model_dao import ModelDAO
from app.models.model_order import OrderType
from tests.commons import db_mock
from tests.commons.db_integration import DatabaseIntegration


class ModelDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_dao = ModelDAO(cls.db)

    def test_insert(self):
        model = db_mock.get_sample_model()
        inserted = self.model_dao.insert(model)
        assert inserted.uuid == model.uuid

    def test_get_by_uuid(self):
        model = db_mock.get_sample_model()
        self.model_dao.insert(model)
        retrieved = self.model_dao.get_by_uuid(model.uuid)
        assert retrieved.uuid == model.uuid

    def test_get_by_uuid_empty(self):
        retrieved = self.model_dao.get_by_uuid(uuid.uuid4())
        assert retrieved is None

    def test_update(self):
        model = db_mock.get_sample_model()
        self.model_dao.insert(model)
        new_features = List[Dict] = [
            {'name': 'feature1', 'type': 'string', 'fieldType': 'categorical'},
            {'name': 'feature2', 'type': 'int', 'fieldType': 'numerical'},
        ]
        updated_rows = self.model_dao.update_features(model.uuid, new_features)
        retrieved = self.model_dao.get_by_uuid(model.uuid)
        assert updated_rows == 1
        assert retrieved.features == new_features

    def test_delete(self):
        model = db_mock.get_sample_model()
        self.model_dao.insert(model)
        rows = self.model_dao.delete(model.uuid)
        retrieved = self.model_dao.get_by_uuid(model.uuid)
        assert rows == 1
        assert retrieved is None

    def test_get_all_paginated(self):
        model1 = db_mock.get_sample_model(id=1, uuid=uuid.uuid4(), name='model1')
        model2 = db_mock.get_sample_model(id=2, uuid=uuid.uuid4(), name='model2')
        model3 = db_mock.get_sample_model(id=3, uuid=uuid.uuid4(), name='model3')
        self.model_dao.insert(model1)
        self.model_dao.insert(model2)
        self.model_dao.insert(model3)
        models = self.model_dao.get_all_paginated()
        assert models.items[0].uuid == model1.uuid
        assert len(models.items) == 3

    def test_get_all_paginated_ordered(self):
        model1 = db_mock.get_sample_model(id=1, uuid=uuid.uuid4(), name='first_model')
        model2 = db_mock.get_sample_model(id=2, uuid=uuid.uuid4(), name='second_model')
        model3 = db_mock.get_sample_model(id=3, uuid=uuid.uuid4(), name='third_model')
        self.model_dao.insert(model1)
        self.model_dao.insert(model2)
        self.model_dao.insert(model3)
        models = self.model_dao.get_all_paginated(order=OrderType.DESC, sort='name')
        assert models.items[0].name == model3.name
        assert len(models.items) == 3
