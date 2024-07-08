import datetime
import unittest
from unittest.mock import MagicMock
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.dataset_dto import (
    CurrentDatasetDTO,
    FileReference,
    OrderType,
    ReferenceDatasetDTO,
)
from app.models.job_status import JobStatus
from app.routes.upload_dataset_route import UploadDatasetRoute
from app.services.file_service import FileService
from tests.commons import csv_file_mock as csv, db_mock


class UploadDatasetRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_service = MagicMock(spec_set=FileService)
        cls.prefix = '/api/models'

        router = UploadDatasetRoute.get_router(cls.file_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app)

    def test_upload_reference(self):
        file = csv.get_correct_sample_csv_file()
        model_uuid = uuid.uuid4()
        upload_file_result = ReferenceDatasetDTO(
            uuid=uuid.uuid4(),
            model_uuid=model_uuid,
            path='test',
            date=str(datetime.datetime.now(tz=datetime.UTC)),
            status=JobStatus.IMPORTING,
        )
        self.file_service.upload_reference_file = MagicMock(
            return_value=upload_file_result
        )
        res = self.client.post(
            f'{self.prefix}/{model_uuid}/reference/upload',
            files={'csv_file': (file.filename, file.file)},
        )
        assert res.status_code == 200
        assert jsonable_encoder(upload_file_result) == res.json()

    def test_bind_reference(self):
        file_ref = FileReference(file_url='/file')
        model_uuid = uuid.uuid4()
        upload_file_result = ReferenceDatasetDTO(
            uuid=uuid.uuid4(),
            model_uuid=model_uuid,
            path='test',
            date=str(datetime.datetime.now(tz=datetime.UTC)),
            status=JobStatus.IMPORTING,
        )
        self.file_service.bind_reference_file = MagicMock(
            return_value=upload_file_result
        )
        res = self.client.post(
            f'{self.prefix}/{model_uuid}/reference/bind',
            json=jsonable_encoder(file_ref),
        )
        assert res.status_code == 200
        assert jsonable_encoder(upload_file_result) == res.json()

    def test_upload_current(self):
        file = csv.get_correct_sample_csv_file()
        model_uuid = uuid.uuid4()
        upload_file_result = CurrentDatasetDTO(
            uuid=uuid.uuid4(),
            model_uuid=model_uuid,
            path='test',
            date=str(datetime.datetime.now(tz=datetime.UTC)),
            status=JobStatus.IMPORTING,
            correlation_id_column=None,
        )
        self.file_service.upload_current_file = MagicMock(
            return_value=upload_file_result
        )
        res = self.client.post(
            f'{self.prefix}/{model_uuid}/current/upload',
            files={'csv_file': (file.filename, file.file)},
        )
        assert res.status_code == 200
        assert jsonable_encoder(upload_file_result) == res.json()

    def test_bind_current(self):
        file_ref = FileReference(file_url='/file')
        model_uuid = uuid.uuid4()
        upload_file_result = CurrentDatasetDTO(
            uuid=uuid.uuid4(),
            model_uuid=model_uuid,
            path='test',
            date=str(datetime.datetime.now(tz=datetime.UTC)),
            status=JobStatus.IMPORTING,
            correlation_id_column=None,
        )
        self.file_service.bind_current_file = MagicMock(return_value=upload_file_result)
        res = self.client.post(
            f'{self.prefix}/{model_uuid}/current/bind',
            json=jsonable_encoder(file_ref),
        )
        assert res.status_code == 200
        assert jsonable_encoder(upload_file_result) == res.json()

    def test_get_all_reference_datasets_by_model_uuid_paginated(self):
        test_model_uuid = uuid.uuid4()
        reference_upload_1 = db_mock.get_sample_reference_dataset(
            model_uuid=test_model_uuid, path='reference/test_1.csv'
        )
        reference_upload_2 = db_mock.get_sample_reference_dataset(
            model_uuid=test_model_uuid, path='reference/test_2.csv'
        )
        reference_upload_3 = db_mock.get_sample_reference_dataset(
            model_uuid=test_model_uuid, path='reference/test_3.csv'
        )

        sample_results = [
            ReferenceDatasetDTO.from_reference_dataset(reference_upload_1),
            ReferenceDatasetDTO.from_reference_dataset(reference_upload_2),
            ReferenceDatasetDTO.from_reference_dataset(reference_upload_3),
        ]
        page = Page.create(
            items=sample_results, total=len(sample_results), params=Params()
        )
        self.file_service.get_all_reference_datasets_by_model_uuid_paginated = (
            MagicMock(return_value=page)
        )

        res = self.client.get(f'{self.prefix}/{test_model_uuid}/reference')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.file_service.get_all_reference_datasets_by_model_uuid_paginated.assert_called_once_with(
            test_model_uuid,
            params=Params(page=1, size=50),
            order=OrderType.ASC,
            sort=None,
        )

    def test_get_all_current_datasets_by_model_uuid_paginated(self):
        test_model_uuid = uuid.uuid4()
        current_upload_1 = db_mock.get_sample_current_dataset(
            model_uuid=test_model_uuid, path='reference/test_1.csv'
        )
        current_upload_2 = db_mock.get_sample_current_dataset(
            model_uuid=test_model_uuid, path='reference/test_2.csv'
        )
        current_upload_3 = db_mock.get_sample_current_dataset(
            model_uuid=test_model_uuid, path='reference/test_3.csv'
        )

        sample_results = [
            CurrentDatasetDTO.from_current_dataset(current_upload_1),
            CurrentDatasetDTO.from_current_dataset(current_upload_2),
            CurrentDatasetDTO.from_current_dataset(current_upload_3),
        ]
        page = Page.create(
            items=sample_results, total=len(sample_results), params=Params()
        )
        self.file_service.get_all_current_datasets_by_model_uuid_paginated = MagicMock(
            return_value=page
        )

        res = self.client.get(f'{self.prefix}/{test_model_uuid}/current')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.file_service.get_all_current_datasets_by_model_uuid_paginated.assert_called_once_with(
            test_model_uuid,
            params=Params(page=1, size=50),
            order=OrderType.ASC,
            sort=None,
        )

    def test_get_all_reference_datasets_by_model_uuid(self):
        test_model_uuid = uuid.uuid4()
        reference_upload_1 = db_mock.get_sample_reference_dataset(
            model_uuid=test_model_uuid, path='reference/test_1.csv'
        )
        reference_upload_2 = db_mock.get_sample_reference_dataset(
            model_uuid=test_model_uuid, path='reference/test_2.csv'
        )
        reference_upload_3 = db_mock.get_sample_reference_dataset(
            model_uuid=test_model_uuid, path='reference/test_3.csv'
        )

        sample_results = [
            ReferenceDatasetDTO.from_reference_dataset(reference_upload_1),
            ReferenceDatasetDTO.from_reference_dataset(reference_upload_2),
            ReferenceDatasetDTO.from_reference_dataset(reference_upload_3),
        ]
        self.file_service.get_all_reference_datasets_by_model_uuid = MagicMock(
            return_value=sample_results
        )

        res = self.client.get(f'{self.prefix}/{test_model_uuid}/reference/all')
        assert res.status_code == 200
        assert jsonable_encoder(sample_results) == res.json()
        self.file_service.get_all_reference_datasets_by_model_uuid.assert_called_once_with(
            test_model_uuid,
        )

    def test_get_all_current_datasets_by_model_uuid(self):
        test_model_uuid = uuid.uuid4()
        current_upload_1 = db_mock.get_sample_current_dataset(
            model_uuid=test_model_uuid, path='reference/test_1.csv'
        )
        current_upload_2 = db_mock.get_sample_current_dataset(
            model_uuid=test_model_uuid, path='reference/test_2.csv'
        )
        current_upload_3 = db_mock.get_sample_current_dataset(
            model_uuid=test_model_uuid, path='reference/test_3.csv'
        )

        sample_results = [
            CurrentDatasetDTO.from_current_dataset(current_upload_1),
            CurrentDatasetDTO.from_current_dataset(current_upload_2),
            CurrentDatasetDTO.from_current_dataset(current_upload_3),
        ]
        self.file_service.get_all_current_datasets_by_model_uuid = MagicMock(
            return_value=sample_results
        )

        res = self.client.get(f'{self.prefix}/{test_model_uuid}/current/all')
        assert res.status_code == 200
        assert jsonable_encoder(sample_results) == res.json()
        self.file_service.get_all_current_datasets_by_model_uuid.assert_called_once_with(
            test_model_uuid,
        )
