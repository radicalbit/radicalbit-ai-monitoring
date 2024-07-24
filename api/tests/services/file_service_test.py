import datetime
import unittest
from unittest.mock import MagicMock
import uuid
from uuid import uuid4

from fastapi import HTTPException
from fastapi_pagination import Page, Params
import pytest

from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.dataset_dto import CurrentDatasetDTO, FileReference, ReferenceDatasetDTO
from app.models.exceptions import InvalidFileException, ModelNotFoundError
from app.models.job_status import JobStatus
from app.models.model_dto import ModelOut
from app.services.file_service import FileService
from app.services.model_service import ModelService
from tests.commons import csv_file_mock as csv, db_mock
from tests.commons.db_mock import get_sample_reference_dataset


class FileServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rd_dao = MagicMock(spec_set=ReferenceDatasetDAO)
        cls.cd_dao = MagicMock(spec_set=CurrentDatasetDAO)
        cls.model_svc = MagicMock(spec_set=ModelService)
        cls.s3_client = MagicMock()
        cls.spark_k8s_client = MagicMock()
        cls.files_service = FileService(
            cls.rd_dao, cls.cd_dao, cls.model_svc, cls.s3_client, cls.spark_k8s_client
        )
        cls.mocks = [
            cls.rd_dao,
            cls.cd_dao,
            cls.model_svc,
            cls.s3_client,
            cls.spark_k8s_client,
        ]

    def test_validate_file_ok(self):
        file = csv.get_correct_sample_csv_file()
        self.files_service.validate_file(file, sep=',', columns=['Name', 'Age'])

    def test_validate_file_error(self):
        file = csv.get_uncorrect_sample_csv_file()
        with pytest.raises(InvalidFileException):
            self.files_service.validate_file(file, sep=',', columns=['a', 'b'])

    def test_infer_schema_ok(self):
        file = csv.get_correct_sample_csv_file()
        schema = FileService.infer_schema(file)

        assert schema == csv.correct_schema()

    def test_infer_schema_error(self):
        file = csv.get_uncorrect_sample_csv_file()

        with pytest.raises(Exception):
            FileService.infer_schema(file)

    def test_infer_schema_separator(self):
        file = csv.get_file_using_sep(';')
        schema = FileService.infer_schema(file, sep=';')
        assert schema == csv.correct_schema()

    def test_upload_reference_file_ok(self):
        file = csv.get_correct_sample_csv_file()
        dataset_uuid = uuid4()
        model = db_mock.get_sample_model()
        object_name = f'{str(model.uuid)}/reference/{dataset_uuid}/{file.filename}'
        path = f's3://bucket/{object_name}'
        inserted_file = ReferenceDataset(
            uuid=dataset_uuid,
            model_uuid=uuid4(),
            path=path,
            date=datetime.datetime.now(tz=datetime.UTC),
            status=JobStatus.IMPORTING,
        )

        self.model_svc.get_model_by_uuid = MagicMock(
            return_value=ModelOut.from_model(model)
        )
        self.s3_client.upload_fileobj = MagicMock()
        self.rd_dao.get_reference_dataset_by_model_uuid = MagicMock(return_value=None)
        self.rd_dao.insert_reference_dataset = MagicMock(return_value=inserted_file)
        self.spark_k8s_client.submit_app = MagicMock()

        result = self.files_service.upload_reference_file(model.uuid, file)

        self.model_svc.get_model_by_uuid.assert_called_once()
        self.rd_dao.get_reference_dataset_by_model_uuid.assert_called_once()
        self.rd_dao.insert_reference_dataset.assert_called_once()
        self.s3_client.upload_fileobj.assert_called_once()
        self.spark_k8s_client.submit_app.assert_called_once()
        assert result == ReferenceDatasetDTO.from_reference_dataset(inserted_file)

    def test_upload_reference_file_model_not_found(self):
        file = csv.get_correct_sample_csv_file()
        self.model_svc.get_model_by_uuid = MagicMock(return_value=None)
        pytest.raises(
            ModelNotFoundError,
            self.files_service.upload_reference_file,
            model_uuid,
            file,
        )

    def test_bind_reference_file_model_not_found(self):
        self.model_svc.get_model_by_uuid = MagicMock(return_value=None)
        pytest.raises(
            ModelNotFoundError,
            self.files_service.bind_reference_file,
            uuid.uuid4(),
            FileReference(file_url='s3://some/file.csv'),
        )

    def test_upload_reference_file_already_exists(self):
        file = csv.get_correct_sample_csv_file()
        dataset_uuid = uuid4()
        model = db_mock.get_sample_model()
        object_name = f'{str(model.uuid)}/reference/{dataset_uuid}/{file.filename}'
        path = f's3://bucket/{object_name}'
        inserted_file = ReferenceDataset(
            uuid=dataset_uuid,
            model_uuid=uuid4(),
            path=path,
            date=datetime.datetime.now(tz=datetime.UTC),
            status=JobStatus.IMPORTING,
        )

        self.rd_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=inserted_file
        )

        pytest.raises(
            HTTPException, self.files_service.upload_reference_file, model.uuid, file
        )

    def test_bind_reference_file_ok(self):
        file_url = f's3://test-bucket/{model_uuid}/reference/test.csv'
        file = FileReference(file_url=file_url)
        model = db_mock.get_sample_model()
        inserted_file = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model_uuid,
            path=file_url,
            date=datetime.datetime.now(tz=datetime.UTC),
            status=JobStatus.IMPORTING,
        )

        self.model_svc.get_model_by_uuid = MagicMock(
            return_value=ModelOut.from_model(model)
        )

        self.s3_client.head_object = MagicMock()
        self.rd_dao.get_reference_dataset_by_model_uuid = MagicMock(return_value=None)
        self.rd_dao.insert_reference_dataset = MagicMock(return_value=inserted_file)

        result = self.files_service.bind_reference_file(model_uuid, file)

        self.rd_dao.get_reference_dataset_by_model_uuid.assert_called_once()
        self.rd_dao.insert_reference_dataset.assert_called_once()
        self.s3_client.head_object.assert_called_once()
        assert result == ReferenceDatasetDTO.from_reference_dataset(inserted_file)

    def test_bind_reference_file_already_exists(self):
        file_url = f's3://test-bucket/{model_uuid}/reference/test.csv'
        file = FileReference(file_url=file_url)
        inserted_file = ReferenceDataset(
            uuid=uuid4(),
            model_uuid=model_uuid,
            path=file_url,
            date=datetime.datetime.now(tz=datetime.UTC),
            status=JobStatus.IMPORTING,
        )

        self.rd_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=inserted_file
        )

        pytest.raises(
            HTTPException, self.files_service.bind_reference_file, model_uuid, file
        )

    def test_upload_current_file_ok(self):
        file = csv.get_current_sample_csv_file()
        model = db_mock.get_sample_model(
            features=[{'name': 'num1', 'type': 'int', 'fieldType': 'numerical'}],
            outputs={
                'prediction': {
                    'name': 'prediction',
                    'type': 'int',
                    'fieldType': 'numerical',
                },
                'prediction_proba': {
                    'name': 'prediction_proba',
                    'type': 'int',
                    'fieldType': 'numerical',
                },
                'output': [{'name': 'num2', 'type': 'int', 'fieldType': 'numerical'}],
            },
            target={'name': 'target', 'type': 'int', 'fieldType': 'numerical'},
            timestamp={'name': 'datetime', 'type': 'datetime', 'fieldType': 'datetime'},
        )
        object_name = f'{str(model.uuid)}/current/{file.filename}'
        path = f's3://bucket/{object_name}'
        inserted_file = CurrentDataset(
            uuid=uuid4(),
            model_uuid=model_uuid,
            path=path,
            date=datetime.datetime.now(tz=datetime.UTC),
            correlation_id_column=None,
            status=JobStatus.IMPORTING,
        )
        reference_file = get_sample_reference_dataset(model_uuid=model_uuid)

        self.model_svc.get_model_by_uuid = MagicMock(
            return_value=ModelOut.from_model(model)
        )
        self.rd_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_file
        )
        self.s3_client.upload_fileobj = MagicMock()
        self.cd_dao.insert_current_dataset = MagicMock(return_value=inserted_file)
        self.spark_k8s_client.submit_app = MagicMock()

        result = self.files_service.upload_current_file(
            model.uuid,
            file,
        )

        self.model_svc.get_model_by_uuid.assert_called_once()
        self.rd_dao.get_reference_dataset_by_model_uuid.assert_called_once()
        self.cd_dao.insert_current_dataset.assert_called_once()
        self.s3_client.upload_fileobj.assert_called_once()
        self.spark_k8s_client.submit_app.assert_called_once()
        assert result == CurrentDatasetDTO.from_current_dataset(inserted_file)

    def test_upload_current_file_reference_file_not_found(self):
        file = csv.get_correct_sample_csv_file()
        correlation_id_column = 'correlation_id'
        model = db_mock.get_sample_model()
        self.model_svc.get_model_by_uuid = MagicMock(return_value=model)
        self.rd_dao.get_reference_dataset_by_model_uuid = MagicMock(return_value=None)
        pytest.raises(
            ModelNotFoundError,
            self.files_service.upload_current_file,
            model_uuid,
            file,
            correlation_id_column,
        )

    def test_get_all_reference_datasets_by_model_uuid_paginated(self):
        reference_upload_1 = db_mock.get_sample_reference_dataset(
            model_uuid=model_uuid, path='reference/test_1.csv'
        )
        reference_upload_2 = db_mock.get_sample_reference_dataset(
            model_uuid=model_uuid, path='reference/test_2.csv'
        )
        reference_upload_3 = db_mock.get_sample_reference_dataset(
            model_uuid=model_uuid, path='reference/test_3.csv'
        )

        sample_results = [reference_upload_1, reference_upload_2, reference_upload_3]
        page = Page.create(
            sample_results, total=len(sample_results), params=Params(page=1, size=10)
        )
        self.rd_dao.get_all_reference_datasets_by_model_uuid_paginated = MagicMock(
            return_value=page
        )

        result = self.files_service.get_all_reference_datasets_by_model_uuid_paginated(
            model_uuid, Params(page=1, size=10)
        )

        assert result.total == 3
        assert len(result.items) == 3
        assert result.items[0].model_uuid == model_uuid
        assert result.items[1].model_uuid == model_uuid
        assert result.items[2].model_uuid == model_uuid

    def test_get_all_current_datasets_by_model_uuid_paginated(self):
        current_upload_1 = db_mock.get_sample_current_dataset(
            model_uuid=model_uuid, path='reference/test_1.csv'
        )
        current_upload_2 = db_mock.get_sample_current_dataset(
            model_uuid=model_uuid, path='reference/test_2.csv'
        )
        current_upload_3 = db_mock.get_sample_current_dataset(
            model_uuid=model_uuid, path='reference/test_3.csv'
        )

        sample_results = [current_upload_1, current_upload_2, current_upload_3]
        page = Page.create(
            sample_results, total=len(sample_results), params=Params(page=1, size=10)
        )
        self.cd_dao.get_all_current_datasets_by_model_uuid_paginated = MagicMock(
            return_value=page
        )

        result = self.files_service.get_all_current_datasets_by_model_uuid_paginated(
            model_uuid, Params(page=1, size=10)
        )

        assert result.total == 3
        assert len(result.items) == 3
        assert result.items[0].model_uuid == model_uuid
        assert result.items[1].model_uuid == model_uuid
        assert result.items[2].model_uuid == model_uuid

    def test_get_all_reference_datasets_by_model_uuid(self):
        reference_upload_1 = db_mock.get_sample_reference_dataset(
            model_uuid=model_uuid, path='reference/test_1.csv'
        )
        reference_upload_2 = db_mock.get_sample_reference_dataset(
            model_uuid=model_uuid, path='reference/test_2.csv'
        )
        reference_upload_3 = db_mock.get_sample_reference_dataset(
            model_uuid=model_uuid, path='reference/test_3.csv'
        )

        sample_results = [reference_upload_1, reference_upload_2, reference_upload_3]
        self.rd_dao.get_all_reference_datasets_by_model_uuid = MagicMock(
            return_value=sample_results
        )

        result = self.files_service.get_all_reference_datasets_by_model_uuid(model_uuid)

        assert len(result) == 3
        assert result[0].model_uuid == model_uuid
        assert result[1].model_uuid == model_uuid
        assert result[2].model_uuid == model_uuid

    def test_get_all_current_datasets_by_model_uuid(self):
        current_upload_1 = db_mock.get_sample_current_dataset(
            model_uuid=model_uuid, path='reference/test_1.csv'
        )
        current_upload_2 = db_mock.get_sample_current_dataset(
            model_uuid=model_uuid, path='reference/test_2.csv'
        )
        current_upload_3 = db_mock.get_sample_current_dataset(
            model_uuid=model_uuid, path='reference/test_3.csv'
        )

        sample_results = [current_upload_1, current_upload_2, current_upload_3]
        self.cd_dao.get_all_current_datasets_by_model_uuid = MagicMock(
            return_value=sample_results
        )

        result = self.files_service.get_all_current_datasets_by_model_uuid(model_uuid)

        assert len(result) == 3
        assert result[0].model_uuid == model_uuid
        assert result[1].model_uuid == model_uuid
        assert result[2].model_uuid == model_uuid


model_uuid = db_mock.MODEL_UUID
