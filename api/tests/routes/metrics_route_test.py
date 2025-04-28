import datetime
import unittest
from unittest.mock import MagicMock
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient

from app.models.dataset_type import DatasetType
from app.models.exceptions import (
    ErrorOut,
    MetricsError,
    MetricsNotFoundError,
    metrics_exception_handler,
)
from app.models.job_status import JobStatus
from app.models.metrics.data_quality_dto import DataQualityDTO
from app.models.metrics.drift_dto import DriftDTO
from app.models.metrics.embeddings_dto import EmbeddingsReportDTO, DriftScore
from app.models.metrics.model_quality_dto import ModelQualityDTO
from app.models.metrics.statistics_dto import StatisticsDTO
from app.models.model_dto import ModelType
from app.routes.metrics_route import MetricsRoute
from app.services.metrics_service import MetricsService
from tests.commons import db_mock


class MetricsRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metrics_service = MagicMock(spec_set=MetricsService)
        cls.prefix = '/api/models'

        router = MetricsRoute.get_router(cls.metrics_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.add_exception_handler(MetricsError, metrics_exception_handler)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app, raise_server_exceptions=False)

    def test_get_reference_statistics_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        reference_metrics = db_mock.get_sample_reference_metrics()
        date = datetime.datetime.now(tz=datetime.UTC)
        statistics = StatisticsDTO.from_dict(
            job_status=JobStatus.SUCCEEDED,
            date=date,
            statistics_data=reference_metrics.statistics,
        )
        self.metrics_service.get_reference_statistics_by_model_by_uuid = MagicMock(
            return_value=statistics
        )

        res = self.client.get(f'{self.prefix}/{model_uuid}/reference/statistics')
        assert res.status_code == 200
        assert jsonable_encoder(statistics) == res.json()
        self.metrics_service.get_reference_statistics_by_model_by_uuid.assert_called_once_with(
            model_uuid
        )

    def test_get_reference_model_quality_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        reference_metrics = db_mock.get_sample_reference_metrics()
        model_quality = ModelQualityDTO.from_dict(
            dataset_type=DatasetType.REFERENCE,
            model_type=ModelType.BINARY,
            job_status=JobStatus.SUCCEEDED,
            model_quality_data=reference_metrics.model_quality,
        )
        self.metrics_service.get_reference_model_quality_by_model_by_uuid = MagicMock(
            return_value=model_quality
        )

        res = self.client.get(f'{self.prefix}/{model_uuid}/reference/model-quality')
        assert res.status_code == 200
        assert jsonable_encoder(model_quality) == res.json()
        self.metrics_service.get_reference_model_quality_by_model_by_uuid.assert_called_once_with(
            model_uuid
        )

    def test_get_reference_data_quality_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        reference_metrics = db_mock.get_sample_reference_metrics()
        data_quality = DataQualityDTO.from_dict(
            model_type=ModelType.BINARY,
            job_status=JobStatus.SUCCEEDED,
            data_quality_data=reference_metrics.data_quality,
        )
        self.metrics_service.get_reference_data_quality_by_model_by_uuid = MagicMock(
            return_value=data_quality
        )

        res = self.client.get(f'{self.prefix}/{model_uuid}/reference/data-quality')
        assert res.status_code == 200
        assert jsonable_encoder(data_quality) == res.json()
        self.metrics_service.get_reference_data_quality_by_model_by_uuid.assert_called_once_with(
            model_uuid
        )

    def test_exception_handler_metrics_not_found_error(self):
        model_uuid = uuid.uuid4()
        self.metrics_service.get_reference_statistics_by_model_by_uuid = MagicMock(
            side_effect=MetricsNotFoundError('error')
        )

        res = self.client.get(f'{self.prefix}/{model_uuid}/reference/statistics')

        assert res.status_code == 404
        assert jsonable_encoder(ErrorOut('error')) == res.json()
        self.metrics_service.get_reference_statistics_by_model_by_uuid.assert_called_once_with(
            model_uuid
        )

    def test_get_current_statistics_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        current_uuid = uuid.uuid4()
        current_metrics = db_mock.get_sample_current_metrics()
        date = datetime.datetime.now(tz=datetime.UTC)
        statistics = StatisticsDTO.from_dict(
            job_status=JobStatus.SUCCEEDED,
            date=date,
            statistics_data=current_metrics.statistics,
        )
        self.metrics_service.get_current_statistics_by_model_by_uuid = MagicMock(
            return_value=statistics
        )

        res = self.client.get(
            f'{self.prefix}/{model_uuid}/current/{current_uuid}/statistics'
        )
        assert res.status_code == 200
        assert jsonable_encoder(statistics) == res.json()
        self.metrics_service.get_current_statistics_by_model_by_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )

    def test_get_current_drift(self):
        current_uuid = uuid.uuid4()
        model = db_mock.get_sample_model()
        current_metrics = db_mock.get_sample_current_metrics()
        drift = DriftDTO.from_dict(
            job_status=JobStatus.SUCCEEDED,
            drift_data=current_metrics.drift,
        )
        self.metrics_service.get_current_drift = MagicMock(return_value=drift)

        res = self.client.get(
            f'{self.prefix}/{model.uuid}/current/{current_uuid}/drift'
        )
        assert res.status_code == 200
        assert jsonable_encoder(drift) == res.json()
        self.metrics_service.get_current_drift.assert_called_once_with(
            model.uuid, current_uuid
        )

    def test_get_current_model_quality_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        current_uuid = uuid.uuid4()
        current_metrics = db_mock.get_sample_current_metrics(
            model_quality=db_mock.binary_current_model_quality_dict
        )
        model_quality = ModelQualityDTO.from_dict(
            dataset_type=DatasetType.CURRENT,
            model_type=ModelType.BINARY,
            job_status=JobStatus.SUCCEEDED,
            model_quality_data=current_metrics.model_quality,
        )
        self.metrics_service.get_current_model_quality_by_model_by_uuid = MagicMock(
            return_value=model_quality
        )

        res = self.client.get(
            f'{self.prefix}/{model_uuid}/current/{current_uuid}/model-quality'
        )
        assert res.status_code == 200
        assert jsonable_encoder(model_quality) == res.json()
        self.metrics_service.get_current_model_quality_by_model_by_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )

    def test_get_current_data_quality_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        current_uuid = uuid.uuid4()
        current_metrics = db_mock.get_sample_current_metrics()
        data_quality = DataQualityDTO.from_dict(
            model_type=ModelType.BINARY,
            job_status=JobStatus.SUCCEEDED,
            data_quality_data=current_metrics.data_quality,
        )
        self.metrics_service.get_current_data_quality_by_model_by_uuid = MagicMock(
            return_value=data_quality
        )

        res = self.client.get(
            f'{self.prefix}/{model_uuid}/current/{current_uuid}/data-quality'
        )
        assert res.status_code == 200
        assert jsonable_encoder(data_quality) == res.json()
        self.metrics_service.get_current_data_quality_by_model_by_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )

    def test_get_completion_model_quality_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        completion_uuid = uuid.uuid4()
        completion_metrics = db_mock.get_sample_completion_metrics()
        model_quality = ModelQualityDTO.from_dict(
            dataset_type=DatasetType.COMPLETION,
            model_type=ModelType.TEXT_GENERATION,
            job_status=JobStatus.SUCCEEDED,
            model_quality_data=completion_metrics.model_quality,
        )
        self.metrics_service.get_completion_model_quality_by_model_by_uuid = MagicMock(
            return_value=model_quality
        )

        res = self.client.get(
            f'{self.prefix}/{model_uuid}/completion/{completion_uuid}/model-quality'
        )
        assert res.status_code == 200
        assert jsonable_encoder(model_quality) == res.json()
        self.metrics_service.get_completion_model_quality_by_model_by_uuid.assert_called_once_with(
            model_uuid, completion_uuid
        )

    def test_get_reference_embeddings_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        reference_metrics = db_mock.get_sample_reference_embeddings_metrics()
        embeddings = EmbeddingsReportDTO.from_dict(
            job_status=JobStatus.SUCCEEDED,
            embeddings_data=reference_metrics.metrics,
            drift_score=None,
        )
        self.metrics_service.get_reference_embeddings_by_model_by_uuid = MagicMock(
            return_value=embeddings
        )

        res = self.client.get(f'{self.prefix}/{model_uuid}/reference/embeddings')
        assert res.status_code == 200
        assert jsonable_encoder(embeddings) == res.json()
        self.metrics_service.get_reference_embeddings_by_model_by_uuid.assert_called_once_with(
            model_uuid
        )

    def test_get_current_embeddings_by_model_by_uuid(self):
        model_uuid = uuid.uuid4()
        current_uuid = uuid.uuid4()
        date = datetime.datetime.now(tz=datetime.UTC)
        current_metrics = db_mock.get_sample_current_embeddings_metrics()
        embeddings = EmbeddingsReportDTO.from_dict(
            job_status=JobStatus.SUCCEEDED,
            embeddings_data=current_metrics.metrics,
            drift_score=DriftScore.from_raw(
                date, current_metrics.drift_score
            ),
        )
        self.metrics_service.get_current_embeddings_by_model_by_uuid = MagicMock(
            return_value=embeddings
        )

        res = self.client.get(f'{self.prefix}/{model_uuid}/current/{current_uuid}/embeddings')
        assert res.status_code == 200
        assert jsonable_encoder(embeddings) == res.json()
        self.metrics_service.get_current_embeddings_by_model_by_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )
