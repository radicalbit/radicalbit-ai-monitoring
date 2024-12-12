import datetime
from uuid import uuid4

from fastapi_pagination import Params

from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.model_dao import ModelDAO
from app.db.tables.completion_dataset_table import CompletionDataset
from tests.commons import db_mock
from tests.commons.db_integration import DatabaseIntegration


class CompletionDatasetDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.completion_dataset_dao = CompletionDatasetDAO(cls.db)
        cls.model_dao = ModelDAO(cls.db)

    def test_insert_completion_dataset_upload_result(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        to_insert = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        inserted = self.completion_dataset_dao.insert_completion_dataset(to_insert)
        assert inserted == to_insert

    def test_get_current_dataset_by_model_uuid(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        to_insert = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        inserted = self.completion_dataset_dao.insert_completion_dataset(to_insert)
        retrieved = self.completion_dataset_dao.get_completion_dataset_by_model_uuid(
            inserted.model_uuid, inserted.uuid
        )
        assert inserted.uuid == retrieved.uuid
        assert inserted.model_uuid == retrieved.model_uuid
        assert inserted.path == retrieved.path

    def test_get_latest_completion_dataset_by_model_uuid(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        completion_one = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        self.completion_dataset_dao.insert_completion_dataset(completion_one)

        completion_two = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )

        inserted_two = self.completion_dataset_dao.insert_completion_dataset(
            completion_two
        )

        retrieved = (
            self.completion_dataset_dao.get_latest_completion_dataset_by_model_uuid(
                model.uuid
            )
        )
        assert inserted_two.uuid == retrieved.uuid
        assert inserted_two.model_uuid == retrieved.model_uuid
        assert inserted_two.path == retrieved.path

    def test_get_all_completion_datasets_by_model_uuid_paginated(self):
        model = self.model_dao.insert(db_mock.get_sample_model())
        completion_upload_1 = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )
        completion_upload_2 = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )
        completion_upload_3 = CompletionDataset(
            uuid=uuid4(),
            model_uuid=model.uuid,
            path='json_file.json',
            date=datetime.datetime.now(tz=datetime.UTC),
        )
        inserted_1 = self.completion_dataset_dao.insert_completion_dataset(
            completion_upload_1
        )
        inserted_2 = self.completion_dataset_dao.insert_completion_dataset(
            completion_upload_2
        )
        inserted_3 = self.completion_dataset_dao.insert_completion_dataset(
            completion_upload_3
        )

        retrieved = self.completion_dataset_dao.get_all_completion_datasets_by_model_uuid_paginated(
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
