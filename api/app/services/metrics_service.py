import datetime
from typing import Optional
from uuid import UUID

from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_metrics_dao import ReferenceDatasetMetricsDAO
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.dataset_type import DatasetType
from app.models.model_dto import ModelType
from app.models.exceptions import MetricsBadRequestError, MetricsInternalError
from app.models.job_status import JobStatus
from app.models.metrics.data_quality_dto import DataQualityDTO
from app.models.metrics.drift_dto import DriftDTO
from app.models.metrics.model_quality_dto import ModelQualityDTO
from app.models.metrics.statistics_dto import StatisticsDTO
from app.services.model_service import ModelService


class MetricsService:
    def __init__(
        self,
        reference_dataset_metrics_dao: ReferenceDatasetMetricsDAO,
        reference_dataset_dao: ReferenceDatasetDAO,
        current_dataset_metrics_dao: CurrentDatasetMetricsDAO,
        current_dataset_dao: CurrentDatasetDAO,
        model_service: ModelService,
    ):
        self.reference_dataset_metrics_dao = reference_dataset_metrics_dao
        self.reference_dataset_dao = reference_dataset_dao
        self.current_dataset_metrics_dao = current_dataset_metrics_dao
        self.current_dataset_dao = current_dataset_dao
        self.model_service = model_service

    def get_reference_statistics_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> StatisticsDTO:
        """
        Retrieve reference statistics for a model by its UUID.
        """
        return self._get_statistics_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_metrics,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_statistics_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> StatisticsDTO:
        """
        Retrieve current statistics for a model by its UUID and an optional current dataset UUID.
        """
        return self._get_statistics_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_reference_model_quality_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> ModelQualityDTO:
        """
        Retrieve reference model quality for a model by its UUID.
        """
        return self._get_model_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_metrics,
            dataset_type=DatasetType.REFERENCE,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_model_quality_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> ModelQualityDTO:
        """
        Retrieve current model quality for a model by its UUID and an optional current dataset UUID.
        """
        return self._get_model_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            dataset_type=DatasetType.CURRENT,
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_reference_data_quality_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> DataQualityDTO:
        """
        Retrieve reference data quality for a model by its UUID.
        """
        return self._get_data_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_metrics,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_data_quality_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DataQualityDTO:
        """
        Retrieve current data quality for a model by its UUID and an optional current dataset UUID.
        """
        return self._get_data_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_current_drift(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DriftDTO:
        """
        Retrieve current drift for a model by its UUID and an optional current dataset UUID.
        """
        return self._get_drift_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_latest_current_uuid(self, model_uuid: UUID) -> Optional[UUID]:
        """
        Retrieve the latest current dataset UUID for a model by its UUID.
        """
        latest_current = (
            self.current_dataset_dao.get_latest_current_dataset_by_model_uuid(
                model_uuid
            )
        )
        return latest_current.uuid if latest_current else None

    def check_and_get_reference_dataset_and_metrics(
        self, model_uuid: UUID
    ) -> tuple[Optional[ReferenceDataset], Optional[ReferenceDatasetMetrics]]:
        """
        Check and retrieve the reference dataset and its metrics for a model by its UUID.
        """
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=self.reference_dataset_dao.get_reference_dataset_by_model_uuid,
            metrics_getter=self.reference_dataset_metrics_dao.get_reference_metrics_by_model_uuid,
        )

    def check_and_get_current_dataset_and_metrics(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> tuple[Optional[CurrentDataset], Optional[CurrentDatasetMetrics]]:
        """
        Check and retrieve the current dataset and its metrics for a model by its UUID and a current dataset UUID.
        """
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=lambda uuid: self.current_dataset_dao.get_current_dataset_by_model_uuid(
                uuid, current_uuid
            ),
            metrics_getter=lambda uuid: self.current_dataset_metrics_dao.get_current_metrics_by_model_uuid(
                uuid, current_uuid
            ),
        )

    @staticmethod
    def _check_and_get_dataset_and_metrics(
        model_uuid: UUID, dataset_getter, metrics_getter
    ) -> tuple[
        Optional[ReferenceDataset | CurrentDataset],
        Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
    ]:
        """
        Check and retrieve the dataset and its metrics using the provided getters.
        """
        dataset = dataset_getter(model_uuid)
        if not dataset:
            return None, None

        if dataset.status == JobStatus.SUCCEEDED:
            metrics = metrics_getter(model_uuid)
            if not metrics:
                raise MetricsBadRequestError(
                    f'Dataset metrics could not be retrieved for model {model_uuid}'
                )
            return dataset, metrics

        if dataset.status in [JobStatus.IMPORTING, JobStatus.ERROR]:
            return dataset, None

        raise MetricsInternalError(f'Invalid dataset status {dataset.status}')

    def _get_statistics_by_model_uuid(
        self,
        model_uuid: UUID,
        dataset_and_metrics_getter,
        missing_status,
    ) -> StatisticsDTO:
        """
        Retrieve statistics for a model by its UUID.
        """
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_statistics_dto(
            dataset=dataset,
            metrics=metrics,
            missing_status=missing_status,
        )

    def _get_model_quality_by_model_uuid(
        self,
        model_uuid: UUID,
        dataset_and_metrics_getter,
        dataset_type: DatasetType,
        missing_status,
    ) -> ModelQualityDTO:
        """
        Retrieve model quality for a model by its UUID.
        """
        model = self.model_service.get_model_by_uuid(model_uuid)
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_model_quality_dto(
            dataset_type=dataset_type,
            model_type=model.model_type,
            dataset=dataset,
            metrics=metrics,
            missing_status=missing_status,
        )

    def _get_data_quality_by_model_uuid(
        self,
        model_uuid: UUID,
        dataset_and_metrics_getter,
        missing_status,
    ) -> DataQualityDTO:
        """
        Retrieve data quality for a model by its UUID.
        """
        model = self.model_service.get_model_by_uuid(model_uuid)
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_data_quality_dto(
            model_type=model.model_type,
            dataset=dataset,
            metrics=metrics,
            missing_status=missing_status,
        )

    def _get_drift_by_model_uuid(
        self,
        model_uuid: UUID,
        dataset_and_metrics_getter,
        missing_status,
    ) -> DriftDTO:
        """
        Retrieve drift for a model by its UUID.
        """
        model = self.model_service.get_model_by_uuid(model_uuid)
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_drift_dto(
            model_type=model.model_type,
            dataset=dataset,
            metrics=metrics,
            missing_status=missing_status,
        )

    @staticmethod
    def _create_statistics_dto(
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> StatisticsDTO:
        """
        Create a StatisticsDTO from the provided dataset and metrics.
        """
        if not dataset:
            return StatisticsDTO.from_dict(
                job_status=missing_status,
                date=datetime.datetime.now(tz=datetime.UTC),
                statistics_data=None,
            )
        if not metrics:
            return StatisticsDTO.from_dict(
                job_status=dataset.status,
                date=dataset.date,
                statistics_data=None,
            )
        return StatisticsDTO.from_dict(
            job_status=dataset.status,
            date=dataset.date,
            statistics_data=metrics.statistics,
        )

    @staticmethod
    def _create_model_quality_dto(
        dataset_type: DatasetType,
        model_type: ModelType,
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> ModelQualityDTO:
        """
        Create a ModelQualityDTO from the provided dataset and metrics.
        """
        if not dataset:
            return ModelQualityDTO.from_dict(
                dataset_type=dataset_type,
                model_type=model_type,
                job_status=missing_status,
                model_quality_data=None,
            )
        if not metrics:
            return ModelQualityDTO.from_dict(
                dataset_type=dataset_type,
                model_type=model_type,
                job_status=dataset.status,
                model_quality_data=None,
            )
        return ModelQualityDTO.from_dict(
            dataset_type=dataset_type,
            model_type=model_type,
            job_status=dataset.status,
            model_quality_data=metrics.model_quality,
        )

    @staticmethod
    def _create_data_quality_dto(
        model_type: ModelType,
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> DataQualityDTO:
        """
        Create a DataQualityDTO from the provided dataset and metrics.
        """
        if not dataset:
            return DataQualityDTO.from_dict(
                model_type=model_type,
                job_status=missing_status,
                data_quality_data=None,
            )
        if not metrics:
            return DataQualityDTO.from_dict(
                model_type=model_type,
                job_status=dataset.status,
                data_quality_data=None,
            )
        return DataQualityDTO.from_dict(
            model_type=model_type,
            job_status=dataset.status,
            data_quality_data=metrics.data_quality,
        )

    @staticmethod
    def _create_drift_dto(
        model_type: ModelType,
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> DriftDTO:
        """
        Create a DriftDTO from the provided dataset and metrics.
        """
        if not dataset:
            return DriftDTO.from_dict(
                model_type=model_type,
                job_status=missing_status,
                drift_data=None,
            )
        if not metrics:
            return DriftDTO.from_dict(
                model_type=model_type,
                job_status=dataset.status,
                drift_data=None,
            )
        return DriftDTO.from_dict(
            model_type=model_type,
            job_status=dataset.status,
            drift_data=metrics.drift,
        )
