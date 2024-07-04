from datetime import datetime
import unittest
from unittest.mock import MagicMock

import pytest

from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_metrics_dao import ReferenceDatasetMetricsDAO
from app.models.dataset_type import DatasetType
from app.models.exceptions import MetricsBadRequestError
from app.models.job_status import JobStatus
from app.models.metrics.data_quality_dto import DataQualityDTO
from app.models.metrics.drift_dto import DriftDTO
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
        cls.model_service: ModelService = MagicMock(spec_set=ModelService)
        cls.metrics_service = MetricsService(
            reference_dataset_metrics_dao=cls.reference_metrics_dao,
            reference_dataset_dao=cls.reference_dataset_dao,
            current_dataset_metrics_dao=cls.current_metrics_dao,
            current_dataset_dao=cls.current_dataset_dao,
            model_service=cls.model_service,
        )
        cls.mocks = [
            cls.reference_metrics_dao,
            cls.reference_dataset_dao,
            cls.current_metrics_dao,
            cls.current_dataset_dao,
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
        current_metrics = db_mock.get_sample_current_metrics(data_quality=db_mock.regression_data_quality_dict)
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


model_uuid = db_mock.MODEL_UUID
current_uuid = db_mock.CURRENT_UUID
