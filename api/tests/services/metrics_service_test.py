from datetime import datetime
import unittest
from unittest.mock import MagicMock

import pytest

from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.completion_dataset_metrics_dao import CompletionDatasetMetricsDAO
from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_embeddings_metrics_dao import (
    CurrentDatasetEmbeddingsMetricsDAO,
)
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_embeddings_metrics_dao import (
    ReferenceDatasetEmbeddingsMetricsDAO,
)
from app.db.dao.reference_dataset_metrics_dao import ReferenceDatasetMetricsDAO
from app.models.dataset_type import DatasetType
from app.models.exceptions import MetricsBadRequestError
from app.models.job_status import JobStatus
from app.models.metrics.data_quality_dto import DataQualityDTO
from app.models.metrics.drift_dto import DriftDTO
from app.models.metrics.embeddings_dto import DriftScore, EmbeddingsReportDTO
from app.models.metrics.model_quality_dto import ModelQualityDTO
from app.models.metrics.statistics_dto import StatisticsDTO
from app.models.model_dto import ModelType
from app.services.metrics_service import MetricsService
from app.services.model_service import ModelService
from tests.commons import db_mock


class MetricsServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference_metrics_dao: ReferenceDatasetMetricsDAO = MagicMock(
            spec_set=ReferenceDatasetMetricsDAO
        )
        cls.reference_dataset_dao: ReferenceDatasetDAO = MagicMock(
            spec_set=ReferenceDatasetDAO
        )
        cls.current_metrics_dao: CurrentDatasetMetricsDAO = MagicMock(
            spec_set=CurrentDatasetMetricsDAO
        )
        cls.current_dataset_dao: CurrentDatasetDAO = MagicMock(
            spec_set=CurrentDatasetDAO
        )
        cls.completion_metrics_dao = MagicMock(spec_set=CompletionDatasetMetricsDAO)
        cls.completion_dataset_dao = MagicMock(spec_set=CompletionDatasetDAO)
        cls.reference_embeddings_metrics_dao = MagicMock(
            spec_set=ReferenceDatasetEmbeddingsMetricsDAO
        )
        cls.current_embeddings_metrics_dao = MagicMock(
            spec_set=CurrentDatasetEmbeddingsMetricsDAO
        )
        cls.model_service: ModelService = MagicMock(spec_set=ModelService)
        cls.metrics_service = MetricsService(
            reference_dataset_metrics_dao=cls.reference_metrics_dao,
            reference_dataset_dao=cls.reference_dataset_dao,
            current_dataset_metrics_dao=cls.current_metrics_dao,
            current_dataset_dao=cls.current_dataset_dao,
            completion_dataset_metrics_dao=cls.completion_metrics_dao,
            completion_dataset_dao=cls.completion_dataset_dao,
            reference_dataset_embeddings_metrics_dao=cls.reference_embeddings_metrics_dao,
            current_dataset_embeddings_metrics_dao=cls.current_embeddings_metrics_dao,
            model_service=cls.model_service,
        )
        cls.mocks = [
            cls.reference_metrics_dao,
            cls.reference_dataset_dao,
            cls.current_metrics_dao,
            cls.current_dataset_dao,
            cls.completion_metrics_dao,
            cls.completion_dataset_dao,
            cls.reference_embeddings_metrics_dao,
            cls.current_embeddings_metrics_dao,
        ]

    def test_get_reference_statistics_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_metrics()
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_statistics_by_model_by_uuid(model_uuid)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == StatisticsDTO.from_dict(
            job_status=status,
            date=reference_dataset.date,
            statistics_data=reference_metrics.statistics,
        )

    def test_get_empty_reference_statistics_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        res = self.metrics_service.get_reference_statistics_by_model_by_uuid(model_uuid)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == StatisticsDTO.from_dict(
            job_status=status,
            date=reference_dataset.date,
            statistics_data=None,
        )

    def test_get_missing_reference_statistics_by_model_by_uuid(self):
        status = JobStatus.MISSING_REFERENCE
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        res = self.metrics_service.get_reference_statistics_by_model_by_uuid(model_uuid)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == StatisticsDTO.from_dict(
            job_status=status,
            date=datetime.strptime(res.date, '%Y-%m-%dT%H:%M:%S.%f%z'),
            statistics_data=None,
        )

    def test_get_reference_statistics_by_model_by_uuid_bad_request(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=None
        )
        pytest.raises(
            MetricsBadRequestError,
            self.metrics_service.get_reference_statistics_by_model_by_uuid,
            model_uuid,
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

    def test_get_reference_binary_class_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_metrics()
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_model_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.REFERENCE,
            model_type=model.model_type,
            job_status=reference_dataset.status,
            model_quality_data=reference_metrics.model_quality,
        )

    def test_get_empty_reference_model_quality_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        res = self.metrics_service.get_reference_model_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.REFERENCE,
            model_type=model.model_type,
            job_status=reference_dataset.status,
            model_quality_data=None,
        )

    def test_get_reference_multiclass_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_metrics(
            model_quality=db_mock.multiclass_model_quality_dict
        )
        model = db_mock.get_sample_model(model_type=ModelType.MULTI_CLASS)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_model_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.REFERENCE,
            model_type=model.model_type,
            job_status=reference_dataset.status,
            model_quality_data=reference_metrics.model_quality,
        )

    def test_get_reference_regression_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_metrics(
            model_quality=db_mock.regression_model_quality_dict
        )
        model = db_mock.get_sample_model(model_type=ModelType.REGRESSION)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_model_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.REFERENCE,
            model_type=model.model_type,
            job_status=reference_dataset.status,
            model_quality_data=reference_metrics.model_quality,
        )

    def test_get_reference_classification_data_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_metrics()
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_data_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=reference_dataset.status,
            data_quality_data=reference_metrics.data_quality,
        )

    def test_get_empty_reference_data_quality_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        res = self.metrics_service.get_reference_data_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=reference_dataset.status,
            data_quality_data=None,
        )

    def test_get_reference_regression_data_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_metrics(
            data_quality=db_mock.regression_data_quality_dict
        )
        model = db_mock.get_sample_model(model_type=ModelType.REGRESSION)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_data_quality_by_model_by_uuid(
            model_uuid
        )
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )
        self.reference_metrics_dao.get_reference_metrics_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=reference_dataset.status,
            data_quality_data=reference_metrics.data_quality,
        )

    def test_get_current_statistics_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics()
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_statistics_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == StatisticsDTO.from_dict(
            job_status=status,
            date=current_dataset.date,
            statistics_data=current_metrics.statistics,
        )

    def test_get_empty_current_statistics_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        res = self.metrics_service.get_current_statistics_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == StatisticsDTO.from_dict(
            job_status=status,
            date=current_dataset.date,
            statistics_data=None,
        )

    def test_get_missing_current_statistics_by_model_by_uuid(self):
        status = JobStatus.MISSING_CURRENT
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        res = self.metrics_service.get_current_statistics_by_model_by_uuid(
            model_uuid, current_uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )

        assert res == StatisticsDTO.from_dict(
            job_status=status,
            date=datetime.strptime(res.date, '%Y-%m-%dT%H:%M:%S.%f%z'),
            statistics_data=None,
        )

    def test_get_current_statistics_by_model_by_uuid_bad_request(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=None
        )
        pytest.raises(
            MetricsBadRequestError,
            self.metrics_service.get_current_statistics_by_model_by_uuid,
            model_uuid,
            current_dataset.uuid,
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

    def test_get_current_drift(self):
        status = JobStatus.SUCCEEDED
        model = db_mock.get_sample_model()
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics()
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_drift(model.uuid, current_dataset.uuid)
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model.uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model.uuid, current_dataset.uuid
        )

        assert res == DriftDTO.from_dict(
            job_status=status,
            drift_data=current_metrics.drift,
        )

    def test_get_empty_current_drift(self):
        status = JobStatus.IMPORTING
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        res = self.metrics_service.get_current_drift(model_uuid, current_dataset.uuid)
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == DriftDTO.from_dict(
            job_status=status,
            drift_data=None,
        )

    def test_get_missing_current_drift(self):
        status = JobStatus.MISSING_CURRENT
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        res = self.metrics_service.get_current_drift(model_uuid, current_uuid)
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )

        assert res == DriftDTO.from_dict(
            job_status=status,
            drift_data=None,
        )

    def test_get_current_drift_bad_request(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=None
        )
        pytest.raises(
            MetricsBadRequestError,
            self.metrics_service.get_current_drift,
            model_uuid,
            current_dataset.uuid,
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

    def test_get_current_classification_data_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics()
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_data_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=current_dataset.status,
            data_quality_data=current_metrics.data_quality,
        )

    def test_get_empty_current_data_quality_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        res = self.metrics_service.get_current_data_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=current_dataset.status,
            data_quality_data=None,
        )

    def test_get_current_regression_data_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics(
            data_quality=db_mock.regression_data_quality_dict
        )
        model = db_mock.get_sample_model(model_type=ModelType.REGRESSION)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_data_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=current_dataset.status,
            data_quality_data=current_metrics.data_quality,
        )

    def test_get_current_binary_class_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics()
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_model_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.CURRENT,
            model_type=model.model_type,
            job_status=current_dataset.status,
            model_quality_data=current_metrics.model_quality,
        )

    def test_get_empty_current_model_quality_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        model = db_mock.get_sample_model()
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        res = self.metrics_service.get_current_model_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.CURRENT,
            model_type=model.model_type,
            job_status=current_dataset.status,
            model_quality_data=None,
        )

    def test_get_current_multiclass_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics(
            model_quality=db_mock.multiclass_model_quality_dict
        )
        model = db_mock.get_sample_model(model_type=ModelType.MULTI_CLASS)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_model_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.CURRENT,
            model_type=model.model_type,
            job_status=current_dataset.status,
            model_quality_data=current_metrics.model_quality,
        )

    def test_get_current_regression_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_metrics(
            model_quality=db_mock.current_regression_model_quality_dict
        )
        model = db_mock.get_sample_model(model_type=ModelType.REGRESSION)
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_model_quality_by_model_by_uuid(
            model_uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )
        self.current_metrics_dao.get_current_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.CURRENT,
            model_type=model.model_type,
            job_status=current_dataset.status,
            model_quality_data=current_metrics.model_quality,
        )

    def test_get_completion_text_generation_model_quality_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        completion_dataset = db_mock.get_sample_completion_dataset(status=status)
        completion_metrics = db_mock.get_sample_completion_metrics()
        model = db_mock.get_sample_model(
            model_type=ModelType.TEXT_GENERATION,
            target=None,
            features=None,
            outputs=None,
            timestamp=None,
        )
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.completion_dataset_dao.get_completion_dataset_by_model_uuid = MagicMock(
            return_value=completion_dataset
        )
        self.completion_metrics_dao.get_completion_metrics_by_model_uuid = MagicMock(
            return_value=completion_metrics
        )
        res = self.metrics_service.get_completion_model_quality_by_model_by_uuid(
            model_uuid, completion_dataset.uuid
        )
        self.completion_dataset_dao.get_completion_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, completion_dataset.uuid
        )
        self.completion_metrics_dao.get_completion_metrics_by_model_uuid.assert_called_once_with(
            model_uuid, completion_dataset.uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.COMPLETION,
            model_type=model.model_type,
            job_status=completion_dataset.status,
            model_quality_data=completion_metrics.model_quality,
        )

    def test_get_empty_completion_model_quality_by_model_by_uuid(self):
        status = JobStatus.IMPORTING
        completion_dataset = db_mock.get_sample_completion_dataset(status=status.value)
        model = db_mock.get_sample_model(
            model_type=ModelType.TEXT_GENERATION,
            target=None,
            features=None,
            outputs=None,
            timestamp=None,
        )
        self.model_service.get_model_by_uuid = MagicMock(return_value=model)
        self.completion_dataset_dao.get_completion_dataset_by_model_uuid = MagicMock(
            return_value=completion_dataset
        )
        res = self.metrics_service.get_completion_model_quality_by_model_by_uuid(
            model_uuid, completion_dataset.uuid
        )
        self.completion_dataset_dao.get_completion_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, completion_dataset.uuid
        )

        assert res == ModelQualityDTO.from_dict(
            dataset_type=DatasetType.COMPLETION,
            model_type=model.model_type,
            job_status=completion_dataset.status,
            model_quality_data=None,
        )

    def test_get_reference_embeddings_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        model = db_mock.get_sample_model()
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        reference_metrics = db_mock.get_sample_reference_embeddings_metrics()
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        self.reference_embeddings_metrics_dao.get_reference_embeddings_metrics_by_model_uuid = MagicMock(
            return_value=reference_metrics
        )
        res = self.metrics_service.get_reference_embeddings_by_model_by_uuid(model.uuid)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model.uuid
        )
        self.reference_embeddings_metrics_dao.get_reference_embeddings_metrics_by_model_uuid.assert_called_once_with(
            model.uuid
        )

        assert res == EmbeddingsReportDTO.from_dict(
            job_status=status,
            embeddings_data=reference_metrics.metrics,
            drift_score=None,
        )

    def test_get_empty_reference_embeddings_by_model_by_uuid(self):
        model = db_mock.get_sample_model()
        status = JobStatus.IMPORTING
        reference_dataset = db_mock.get_sample_reference_dataset(status=status.value)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=reference_dataset
        )
        res = self.metrics_service.get_reference_embeddings_by_model_by_uuid(model.uuid)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == EmbeddingsReportDTO.from_dict(
            job_status=status,
            embeddings_data=None,
            drift_score=None,
        )

    def test_get_missing_reference_embeddings(self):
        status = JobStatus.MISSING_REFERENCE
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        res = self.metrics_service.get_reference_embeddings_by_model_by_uuid(model_uuid)
        self.reference_dataset_dao.get_reference_dataset_by_model_uuid.assert_called_once_with(
            model_uuid
        )

        assert res == EmbeddingsReportDTO.from_dict(
            job_status=status,
            embeddings_data=None,
            drift_score=None,
        )

    def test_get_current_embeddings_by_model_by_uuid(self):
        status = JobStatus.SUCCEEDED
        model = db_mock.get_sample_model()
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        current_metrics = db_mock.get_sample_current_embeddings_metrics()
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        self.current_embeddings_metrics_dao.get_current_embeddings_metrics_by_model_uuid = MagicMock(
            return_value=current_metrics
        )
        res = self.metrics_service.get_current_embeddings_by_model_by_uuid(
            model.uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model.uuid, current_dataset.uuid
        )
        self.current_embeddings_metrics_dao.get_current_embeddings_metrics_by_model_uuid.assert_called_once_with(
            model.uuid, current_dataset.uuid
        )

        assert res == EmbeddingsReportDTO.from_dict(
            job_status=status,
            embeddings_data=current_metrics.metrics,
            drift_score=DriftScore.from_raw(
                current_dataset.date, current_metrics.drift_score
            ),
        )

    def test_get_empty_current_embeddings_by_model_by_uuid(self):
        model = db_mock.get_sample_model()
        status = JobStatus.IMPORTING
        current_dataset = db_mock.get_sample_current_dataset(status=status.value)
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=current_dataset
        )
        res = self.metrics_service.get_current_embeddings_by_model_by_uuid(
            model.uuid, current_dataset.uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_dataset.uuid
        )

        assert res == EmbeddingsReportDTO.from_dict(
            job_status=status,
            embeddings_data=None,
            drift_score=None,
        )

    def test_get_missing_current_embeddings(self):
        status = JobStatus.MISSING_CURRENT
        self.current_dataset_dao.get_current_dataset_by_model_uuid = MagicMock(
            return_value=None
        )
        res = self.metrics_service.get_current_embeddings_by_model_by_uuid(
            model_uuid, current_uuid
        )
        self.current_dataset_dao.get_current_dataset_by_model_uuid.assert_called_once_with(
            model_uuid, current_uuid
        )

        assert res == EmbeddingsReportDTO.from_dict(
            job_status=status,
            embeddings_data=None,
            drift_score=None,
        )


model_uuid = db_mock.MODEL_UUID
current_uuid = db_mock.CURRENT_UUID
