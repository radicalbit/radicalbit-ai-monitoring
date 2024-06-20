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
        reference_dataset, reference_metrics = (
            self.check_and_get_reference_dataset_and_metrics(model_uuid)
        )
        if not reference_dataset:
            return StatisticsDTO.from_dict(
                job_status=JobStatus.MISSING_REFERENCE,
                date=datetime.datetime.now(tz=datetime.UTC),
                statistics_data=None,
            )
        if not reference_metrics:
            return StatisticsDTO.from_dict(
                job_status=reference_dataset.status,
                date=reference_dataset.date,
                statistics_data=None,
            )
        return StatisticsDTO.from_dict(
            job_status=reference_dataset.status,
            date=reference_dataset.date,
            statistics_data=reference_metrics.statistics,
        )

    def get_reference_model_quality_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> ModelQualityDTO:
        model = self.model_service.get_model_by_uuid(model_uuid)
        reference_dataset, reference_metrics = (
            self.check_and_get_reference_dataset_and_metrics(model_uuid)
        )
        if not reference_dataset:
            return ModelQualityDTO.from_dict(
                model_type=model.model_type,
                job_status=JobStatus.MISSING_REFERENCE,
                model_quality_data=None,
            )
        if not reference_metrics:
            return ModelQualityDTO.from_dict(
                model_type=model.model_type,
                job_status=reference_dataset.status,
                model_quality_data=None,
            )
        return ModelQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=reference_dataset.status,
            model_quality_data=reference_metrics.model_quality,
        )

    def get_reference_data_quality_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> DataQualityDTO:
        model = self.model_service.get_model_by_uuid(model_uuid)
        reference_dataset, reference_metrics = (
            self.check_and_get_reference_dataset_and_metrics(model_uuid)
        )
        if not reference_dataset:
            return DataQualityDTO.from_dict(
                model_type=model.model_type,
                job_status=JobStatus.MISSING_REFERENCE,
                data_quality_data=None,
            )
        if not reference_metrics:
            return DataQualityDTO.from_dict(
                model_type=model.model_type,
                job_status=reference_dataset.status,
                data_quality_data=None,
            )
        return DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=reference_dataset.status,
            data_quality_data=reference_metrics.data_quality,
        )

    def get_current_drift(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DriftDTO:
        model = self.model_service.get_model_by_uuid(model_uuid)
        if current_uuid is None:
            latest_current = (
                self.current_dataset_dao.get_latest_current_dataset_by_model_uuid(
                    model_uuid
                )
            )
            if latest_current is None:
                return DriftDTO.from_dict(
                    model_type=model.model_type,
                    job_status=JobStatus.MISSING_CURRENT,
                    drift_data=None,
                )

            current_uuid = latest_current.uuid

        current_dataset, current_metrics = (
            self.check_and_get_current_dataset_and_metrics(model_uuid, current_uuid)
        )
        if not current_dataset:
            return DriftDTO.from_dict(
                model_type=model.model_type,
                job_status=JobStatus.MISSING_CURRENT,
                drift_data=None,
            )
        if not current_metrics:
            return DriftDTO.from_dict(
                model_type=model.model_type,
                job_status=current_dataset.status,
                drift_data=None,
            )
        return DriftDTO.from_dict(
            model_type=model.model_type,
            job_status=current_dataset.status,
            drift_data=current_metrics.drift,
        )

    def check_and_get_reference_dataset_and_metrics(
        self, model_uuid: UUID
    ) -> tuple[Optional[ReferenceDataset], Optional[ReferenceDatasetMetrics]]:
        reference_dataset = (
            self.reference_dataset_dao.get_reference_dataset_by_model_uuid(model_uuid)
        )
        if not reference_dataset:
            return None, None
        match reference_dataset.status:
            case JobStatus.IMPORTING:
                return reference_dataset, None
            case JobStatus.SUCCEEDED:
                reference_metrics = self.reference_dataset_metrics_dao.get_reference_metrics_by_model_uuid(
                    model_uuid
                )
                if not reference_metrics:
                    raise MetricsBadRequestError(
                        f'Reference dataset metrics could not be retrieved for model {model_uuid}'
                    )
                return reference_dataset, reference_metrics
            case JobStatus.ERROR:
                return reference_dataset, None
            case _:
                raise MetricsInternalError(
                    f'Invalid reference dataset status {reference_dataset.status}'
                )

    def get_current_statistics_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> StatisticsDTO:
        if current_uuid is None:
            latest_current = (
                self.current_dataset_dao.get_latest_current_dataset_by_model_uuid(
                    model_uuid
                )
            )
            if latest_current is None:
                return StatisticsDTO.from_dict(
                    job_status=JobStatus.MISSING_CURRENT,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    statistics_data=None,
                )

            current_uuid = latest_current.uuid
        current_dataset, current_metrics = (
            self.check_and_get_current_dataset_and_metrics(model_uuid, current_uuid)
        )

        if not current_dataset:
            return StatisticsDTO.from_dict(
                job_status=JobStatus.MISSING_CURRENT,
                date=datetime.datetime.now(tz=datetime.UTC),
                statistics_data=None,
            )
        if not current_metrics:
            return StatisticsDTO.from_dict(
                job_status=current_dataset.status,
                date=current_dataset.date,
                statistics_data=None,
            )
        return StatisticsDTO.from_dict(
            job_status=current_dataset.status,
            date=current_dataset.date,
            statistics_data=current_metrics.statistics,
        )

    def get_current_model_quality_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DataQualityDTO:
        model = self.model_service.get_model_by_uuid(model_uuid)
        if current_uuid is None:
            latest_current = (
                self.current_dataset_dao.get_latest_current_dataset_by_model_uuid(
                    model_uuid
                )
            )
            if latest_current is None:
                return ModelQualityDTO.from_dict(
                    dataset_type=DatasetType.CURRENT,
                    model_type=model.model_type,
                    job_status=JobStatus.MISSING_CURRENT,
                    model_quality_data=None,
                )

            current_uuid = latest_current.uuid
        current_dataset, current_metrics = (
            self.check_and_get_current_dataset_and_metrics(model_uuid, current_uuid)
        )
        if not current_dataset:
            return ModelQualityDTO.from_dict(
                dataset_type=DatasetType.CURRENT,
                model_type=model.model_type,
                job_status=JobStatus.MISSING_CURRENT,
                model_quality_data=None,
            )
        if not current_metrics:
            return ModelQualityDTO.from_dict(
                dataset_type=DatasetType.CURRENT,
                model_type=model.model_type,
                job_status=current_dataset.status,
                model_quality_data=None,
            )
        return ModelQualityDTO.from_dict(
            dataset_type=DatasetType.CURRENT,
            model_type=model.model_type,
            job_status=current_dataset.status,
            model_quality_data=current_metrics.model_quality,
        )

    def get_current_data_quality_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DataQualityDTO:
        model = self.model_service.get_model_by_uuid(model_uuid)
        if current_uuid is None:
            latest_current = (
                self.current_dataset_dao.get_latest_current_dataset_by_model_uuid(
                    model_uuid
                )
            )
            if latest_current is None:
                return DataQualityDTO.from_dict(
                    model_type=model.model_type,
                    job_status=JobStatus.MISSING_CURRENT,
                    data_quality_data=None,
                )

            current_uuid = latest_current.uuid

        current_dataset, current_metrics = (
            self.check_and_get_current_dataset_and_metrics(model_uuid, current_uuid)
        )

        if not current_dataset:
            return DataQualityDTO.from_dict(
                model_type=model.model_type,
                job_status=JobStatus.MISSING_CURRENT,
                data_quality_data=None,
            )
        if not current_metrics:
            return DataQualityDTO.from_dict(
                model_type=model.model_type,
                job_status=current_dataset.status,
                data_quality_data=None,
            )
        return DataQualityDTO.from_dict(
            model_type=model.model_type,
            job_status=current_dataset.status,
            data_quality_data=current_metrics.data_quality,
        )

    def check_and_get_current_dataset_and_metrics(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> tuple[Optional[CurrentDataset], Optional[CurrentDatasetMetrics]]:
        current_dataset = self.current_dataset_dao.get_current_dataset_by_model_uuid(
            model_uuid, current_uuid
        )
        if not current_dataset:
            return None, None
        match current_dataset.status:
            case JobStatus.IMPORTING:
                return current_dataset, None
            case JobStatus.SUCCEEDED:
                current_metrics = (
                    self.current_dataset_metrics_dao.get_current_metrics_by_model_uuid(
                        model_uuid, current_uuid
                    )
                )
                if not current_metrics:
                    raise MetricsBadRequestError(
                        f'Current dataset metrics could not be retrieved for model {model_uuid}'
                    )
                return current_dataset, current_metrics
            case JobStatus.ERROR:
                return current_dataset, None
            case _:
                raise MetricsInternalError(
                    f'Invalid current dataset status {current_dataset.status}'
                )
