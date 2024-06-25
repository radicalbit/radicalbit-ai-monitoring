import datetime
from uuid import uuid4

from fastapi_pagination import Params

from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.tables.reference_dataset_table import ReferenceDataset
from tests.commons import db_mock
from tests.commons.db_integration import DatabaseIntegration


class ReferenceDatasetDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reference_dataset_dao = ReferenceDatasetDAO(cls.db)
        cls.model_dao = ModelDAO(cls.db)

    def test_insert_reference_dataset_upload_result(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        to_insert = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        inserted = self.reference_dataset_dao.insert_reference_dataset(to_insert)
        assert inserted == to_insert

    def test_get_reference_dataset_by_model_uuid(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        to_insert = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        inserted = self.reference_dataset_dao.insert_reference_dataset(to_insert)
        retrieved = self.reference_dataset_dao.get_reference_dataset_by_model_uuid(
            inserted.model_uuid
        )
        assert inserted.uuid == retrieved.uuid
        assert inserted.model_uuid == retrieved.model_uuid
        assert inserted.path == retrieved.path

    def test_get_latest_reference_dataset_by_model_uuid(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        reference_one = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        self.reference_dataset_dao.insert_reference_dataset(reference_one)

        reference_two = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        inserted_two = self.reference_dataset_dao.insert_reference_dataset(
            reference_two
        )

        retrieved = (
            self.reference_dataset_dao.get_latest_reference_dataset_by_model_uuid(
                model.uuid
            )
        )
        assert inserted_two.uuid == retrieved.uuid
        assert inserted_two.model_uuid == retrieved.model_uuid
        assert inserted_two.path == retrieved.path

    def test_get_all_reference_datasets_by_model_uuid_paginated(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        reference_upload_1 = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )
        reference_upload_2 = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )
        reference_upload_3 = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='frank_file.csv',
            date=datetime.datetime.now(tz=datetime.UTC),
        )
        inserted_1 = self.reference_dataset_dao.insert_reference_dataset(
            reference_upload_1
        )
        inserted_2 = self.reference_dataset_dao.insert_reference_dataset(
            reference_upload_2
        )
        inserted_3 = self.reference_dataset_dao.insert_reference_dataset(
            reference_upload_3
        )

        retrieved = self.reference_dataset_dao.get_all_reference_datasets_by_model_uuid_paginated(
            model.uuid, Params(page=1, size=10)
        )

        assert inserted_1.uuid == retrieved.items[0].uuid
        assert inserted_1.model_uuid == retrieved.items[0].model_uuid
        assert inserted_1.path == retrieved.items[0].path

        assert inserted_2.uuid == retrieved.items[1].uuid
        assert inserted_2.model_uuid == retrieved.items[1].model_uuid
        assert inserted_2.path == retrieved.items[1].path

        assert inserted_3.uuid == retrieved.items[2].uuid
        assert inserted_3.model_uuid == retrieved.items[2].model_uuid
        assert inserted_3.path == retrieved.items[2].path

        assert len(retrieved.items) == 3
