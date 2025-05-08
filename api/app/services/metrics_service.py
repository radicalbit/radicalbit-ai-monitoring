from datetime import UTC, datetime
from typing import Optional
from uuid import UUID

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
from app.db.tables.completion_dataset_metrics_table import CompletionDatasetMetrics
from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_embeddings_metrics_table import (
    CurrentDatasetEmbeddingsMetrics,
)
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.reference_dataset_embeddings_metrics_table import (
    ReferenceDatasetEmbeddingsMetrics,
)
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.dataset_type import DatasetType
from app.models.exceptions import MetricsBadRequestError, MetricsInternalError
from app.models.job_status import JobStatus
from app.models.metrics.data_quality_dto import DataQualityDTO
from app.models.metrics.drift_dto import DriftDTO
from app.models.metrics.embeddings_dto import (
    DriftScore,
    EmbeddingsDriftDTO,
    EmbeddingsReportDTO,
)
from app.models.metrics.model_quality_dto import ModelQualityDTO
from app.models.metrics.percentages_dto import PercentagesDTO
from app.models.metrics.statistics_dto import StatisticsDTO
from app.models.model_dto import ModelType
from app.services.model_service import ModelService


class MetricsService:
    def __init__(
        self,
        reference_dataset_metrics_dao: ReferenceDatasetMetricsDAO,
        reference_dataset_dao: ReferenceDatasetDAO,
        current_dataset_metrics_dao: CurrentDatasetMetricsDAO,
        current_dataset_dao: CurrentDatasetDAO,
        completion_dataset_metrics_dao: CompletionDatasetMetricsDAO,
        completion_dataset_dao: CompletionDatasetDAO,
        reference_dataset_embeddings_metrics_dao: ReferenceDatasetEmbeddingsMetricsDAO,
        current_dataset_embeddings_metrics_dao: CurrentDatasetEmbeddingsMetricsDAO,
        model_service: ModelService,
    ):
        self.reference_dataset_metrics_dao = reference_dataset_metrics_dao
        self.reference_dataset_dao = reference_dataset_dao
        self.current_dataset_metrics_dao = current_dataset_metrics_dao
        self.current_dataset_dao = current_dataset_dao
        self.completion_dataset_metrics_dao = completion_dataset_metrics_dao
        self.completion_dataset_dao = completion_dataset_dao
        self.reference_dataset_embeddings_metrics_dao = (
            reference_dataset_embeddings_metrics_dao
        )
        self.current_dataset_embeddings_metrics_dao = (
            current_dataset_embeddings_metrics_dao
        )
        self.model_service = model_service

    def get_reference_statistics_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> StatisticsDTO:
        """Retrieve reference statistics for a model by its UUID."""
        return self._get_statistics_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_metrics,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_statistics_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> StatisticsDTO:
        """Retrieve current statistics for a model by its UUID and an optional current dataset UUID."""
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
        """Retrieve reference model quality for a model by its UUID."""
        return self._get_model_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_metrics,
            dataset_type=DatasetType.REFERENCE,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_model_quality_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> ModelQualityDTO:
        """Retrieve current model quality for a model by its UUID and an optional current dataset UUID."""
        return self._get_model_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            dataset_type=DatasetType.CURRENT,
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_completion_model_quality_by_model_by_uuid(
        self, model_uuid: UUID, completion_uuid: UUID
    ) -> ModelQualityDTO:
        """Retrieve completion model quality for a model by its UUID."""
        return self._get_model_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_completion_dataset_and_metrics(
                uuid, completion_uuid
            ),
            dataset_type=DatasetType.COMPLETION,
            missing_status=JobStatus.MISSING_COMPLETION,
        )

    def get_reference_data_quality_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> DataQualityDTO:
        """Retrieve reference data quality for a model by its UUID."""
        return self._get_data_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_metrics,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_data_quality_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DataQualityDTO:
        """Retrieve current data quality for a model by its UUID and an optional current dataset UUID."""
        return self._get_data_quality_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_current_percentages_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> PercentagesDTO:
        """Retrieve current percentages for a model by its UUID and an optional current dataset UUID."""
        return self._get_percentages_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_current_drift(
        self, model_uuid: UUID, current_uuid: Optional[UUID]
    ) -> DriftDTO:
        """Retrieve current drift for a model by its UUID and an optional current dataset UUID."""
        return self._get_drift_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_reference_embeddings_by_model_by_uuid(
        self, model_uuid: UUID
    ) -> EmbeddingsReportDTO:
        """Retrieve reference embeddings for a model by its UUID."""
        return self._get_embeddings_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=self.check_and_get_reference_dataset_and_embeddings_metrics,
            missing_status=JobStatus.MISSING_REFERENCE,
        )

    def get_current_embeddings_by_model_by_uuid(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> EmbeddingsReportDTO:
        """Retrieve current embeddings for a model by its UUID."""
        return self._get_embeddings_by_model_uuid(
            model_uuid=model_uuid,
            dataset_and_metrics_getter=lambda uuid: self.check_and_get_current_dataset_and_embeddings_metrics(
                uuid, current_uuid
            ),
            missing_status=JobStatus.MISSING_CURRENT,
        )

    def get_current_embeddings_drift_by_model_by_uuid(
        self,
        model_uuid: UUID,
    ) -> EmbeddingsDriftDTO:
        """Retrieve current embeddings drift for a model by its UUID."""
        datasets, metrics_list = (
            self.check_and_get_all_current_dataset_and_embeddings_metrics(model_uuid)
        )

        return self._create_embeddings_drift_dto(
            datasets,
            metrics_list,
        )

    def check_and_get_reference_dataset_and_metrics(
        self, model_uuid: UUID
    ) -> tuple[Optional[ReferenceDataset], Optional[ReferenceDatasetMetrics]]:
        """Check and retrieve the reference dataset and its metrics for a model by its UUID."""
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=self.reference_dataset_dao.get_reference_dataset_by_model_uuid,
            metrics_getter=self.reference_dataset_metrics_dao.get_reference_metrics_by_model_uuid,
        )

    def check_and_get_current_dataset_and_metrics(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> tuple[Optional[CurrentDataset], Optional[CurrentDatasetMetrics]]:
        """Check and retrieve the current dataset and its metrics for a model by its UUID and a current dataset UUID."""
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=lambda uuid: self.current_dataset_dao.get_current_dataset_by_model_uuid(
                uuid, current_uuid
            ),
            metrics_getter=lambda uuid: self.current_dataset_metrics_dao.get_current_metrics_by_model_uuid(
                uuid, current_uuid
            ),
        )

    def check_and_get_completion_dataset_and_metrics(
        self, model_uuid: UUID, completion_uuid: UUID
    ) -> tuple[Optional[CompletionDataset], Optional[CompletionDatasetMetrics]]:
        """Check and retrieve the completion dataset and its metrics for a model by its UUID."""
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=lambda uuid: self.completion_dataset_dao.get_completion_dataset_by_model_uuid(
                uuid, completion_uuid
            ),
            metrics_getter=lambda uuid: self.completion_dataset_metrics_dao.get_completion_metrics_by_model_uuid(
                uuid, completion_uuid
            ),
        )

    def check_and_get_reference_dataset_and_embeddings_metrics(
        self, model_uuid: UUID
    ) -> tuple[Optional[ReferenceDataset], Optional[ReferenceDatasetEmbeddingsMetrics]]:
        """Check and retrieve the reference dataset and its embeddings metrics for a model by its UUID."""
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=self.reference_dataset_dao.get_reference_dataset_by_model_uuid,
            metrics_getter=self.reference_dataset_embeddings_metrics_dao.get_reference_embeddings_metrics_by_model_uuid,
        )

    def check_and_get_current_dataset_and_embeddings_metrics(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> tuple[Optional[CurrentDataset], Optional[CurrentDatasetEmbeddingsMetrics]]:
        """Check and retrieve the current dataset and its embeddings metrics for a model by its UUID and a current dataset UUID."""
        return self._check_and_get_dataset_and_metrics(
            model_uuid=model_uuid,
            dataset_getter=lambda uuid: self.current_dataset_dao.get_current_dataset_by_model_uuid(
                uuid, current_uuid
            ),
            metrics_getter=lambda uuid: self.current_dataset_embeddings_metrics_dao.get_current_embeddings_metrics_by_model_uuid(
                uuid, current_uuid
            ),
        )

    def check_and_get_all_current_dataset_and_embeddings_metrics(
        self, model_uuid: UUID
    ) -> tuple[list[CurrentDataset], list[CurrentDatasetEmbeddingsMetrics]]:
        """Retrieve all current datasets and their embeddings metrics for a model by its UUID, only if their status is SUCCEEDED."""

        datasets = self.current_dataset_dao.get_all_current_datasets_by_model_uuid(
            model_uuid
        )
        if not datasets:
            return [], []

        succeeded_datasets = [d for d in datasets if d.status == JobStatus.SUCCEEDED]
        if not succeeded_datasets:
            return [], []

        metrics_list: list[CurrentDatasetEmbeddingsMetrics] = [
            metrics
            for dataset in succeeded_datasets
            if (
                metrics
                := self.current_dataset_embeddings_metrics_dao.get_current_embeddings_metrics_by_model_uuid(
                    model_uuid, dataset.uuid
                )
            )
        ]

        return succeeded_datasets, metrics_list

    @staticmethod
    def _check_and_get_dataset_and_metrics(
        model_uuid: UUID, dataset_getter, metrics_getter
    ) -> tuple[
        Optional[ReferenceDataset | CurrentDataset | CompletionDataset],
        Optional[
            ReferenceDatasetMetrics | CurrentDatasetMetrics | CompletionDatasetMetrics
        ],
    ]:
        """Check and retrieve the dataset and its metrics using the provided getters."""
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
        """Retrieve statistics for a model by its UUID."""
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
        """Retrieve model quality for a model by its UUID."""
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
        """Retrieve data quality for a model by its UUID."""
        model = self.model_service.get_model_by_uuid(model_uuid)
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_data_quality_dto(
            model_type=model.model_type,
            dataset=dataset,
            metrics=metrics,
            missing_status=missing_status,
        )

    def _get_percentages_by_model_uuid(
        self,
        model_uuid: UUID,
        dataset_and_metrics_getter,
        missing_status,
    ) -> PercentagesDTO:
        """Retrieve data quality for a model by its UUID."""
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_percentages_dto(
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
        """Retrieve drift for a model by its UUID."""
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_drift_dto(
            dataset=dataset,
            metrics=metrics,
            missing_status=missing_status,
        )

    def _get_embeddings_by_model_uuid(
        self, model_uuid: UUID, dataset_and_metrics_getter, missing_status
    ) -> EmbeddingsReportDTO:
        dataset, metrics = dataset_and_metrics_getter(model_uuid)
        return self._create_embeddings_dto(
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
        """Create a StatisticsDTO from the provided dataset and metrics."""
        job_status = dataset.status if dataset else missing_status
        dataset_date = dataset.date if dataset else datetime.now(tz=UTC)

        if not dataset or not metrics:
            return StatisticsDTO.from_dict(
                job_status=job_status,
                date=dataset_date,
                statistics_data=None,
            )

        return StatisticsDTO.from_dict(
            job_status=job_status,
            date=dataset_date,
            statistics_data=metrics.statistics,
        )

    @staticmethod
    def _create_model_quality_dto(
        dataset_type: DatasetType,
        model_type: ModelType,
        dataset: Optional[ReferenceDataset | CurrentDataset | CompletionDataset],
        metrics: Optional[
            ReferenceDatasetMetrics | CurrentDatasetMetrics | CompletionDatasetMetrics
        ],
        missing_status,
    ) -> ModelQualityDTO:
        """Create a ModelQualityDTO from the provided dataset and metrics."""
        job_status = dataset.status if dataset else missing_status

        if not dataset or not metrics:
            return ModelQualityDTO.from_dict(
                dataset_type=dataset_type,
                model_type=model_type,
                job_status=job_status,
                model_quality_data=None,
            )

        return ModelQualityDTO.from_dict(
            dataset_type=dataset_type,
            model_type=model_type,
            job_status=job_status,
            model_quality_data=metrics.model_quality,
        )

    @staticmethod
    def _create_data_quality_dto(
        model_type: ModelType,
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> DataQualityDTO:
        """Create a DataQualityDTO from the provided dataset and metrics."""
        job_status = dataset.status if dataset else missing_status

        if not dataset or not metrics:
            return DataQualityDTO.from_dict(
                model_type=model_type,
                job_status=job_status,
                data_quality_data=None,
            )

        return DataQualityDTO.from_dict(
            model_type=model_type,
            job_status=job_status,
            data_quality_data=metrics.data_quality,
        )

    @staticmethod
    def _create_percentages_dto(
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> PercentagesDTO:
        """Create a PercentagesDTO from the provided dataset and metrics."""
        job_status = dataset.status if dataset else missing_status

        if not dataset or not metrics:
            return PercentagesDTO.from_dict(
                job_status=job_status,
                percentages_data=None,
            )

        return PercentagesDTO.from_dict(
            job_status=job_status,
            percentages_data=metrics.percentages,
        )

    @staticmethod
    def _create_drift_dto(
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[ReferenceDatasetMetrics | CurrentDatasetMetrics],
        missing_status,
    ) -> DriftDTO:
        """Create a DriftDTO from the provided dataset and metrics."""
        job_status = dataset.status if dataset else missing_status

        if not dataset or not metrics:
            return DriftDTO.from_dict(
                job_status=job_status,
                drift_data=None,
            )

        return DriftDTO.from_dict(
            job_status=job_status,
            drift_data=metrics.drift,
        )

    @staticmethod
    def _create_embeddings_dto(
        dataset: Optional[ReferenceDataset | CurrentDataset],
        metrics: Optional[
            ReferenceDatasetEmbeddingsMetrics | CurrentDatasetEmbeddingsMetrics
        ],
        missing_status,
    ) -> EmbeddingsReportDTO:
        """Create a EmbeddingsReportDTO from the provided dataset and metrics."""
        job_status = dataset.status if dataset else missing_status

        if not dataset or not metrics:
            return EmbeddingsReportDTO.from_dict(
                job_status=job_status,
                embeddings_data=None,
                drift_score=None,
            )

        drift_score = (
            DriftScore.from_raw(dataset.date, metrics.drift_score)
            if isinstance(metrics, CurrentDatasetEmbeddingsMetrics)
            and metrics.drift_score is not None
            else None
        )

        return EmbeddingsReportDTO.from_dict(
            job_status=job_status,
            embeddings_data=metrics.metrics,
            drift_score=drift_score,
        )

    @staticmethod
    def _create_embeddings_drift_dto(
        datasets: list[CurrentDataset],
        metrics_list: list[CurrentDatasetEmbeddingsMetrics],
    ) -> EmbeddingsDriftDTO:
        """Create a EmbeddingsDriftDTO from the provided dataset and metrics."""
        drift_scores = [
            DriftScore.from_raw(dataset.date, metrics.drift_score)
            for dataset, metrics in zip(datasets, metrics_list)
            if metrics.drift_score is not None
        ]

        return EmbeddingsDriftDTO.from_drift_scores(drift_scores)
