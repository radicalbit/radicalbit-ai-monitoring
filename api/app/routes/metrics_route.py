import logging
from uuid import UUID

from fastapi import APIRouter

from app.core import get_config
from app.models.metrics.data_quality_dto import DataQualityDTO
from app.models.metrics.drift_dto import DriftDTO
from app.models.metrics.embeddings_dto import EmbeddingsReportDTO
from app.models.metrics.model_quality_dto import ModelQualityDTO
from app.models.metrics.percentages_dto import PercentagesDTO
from app.models.metrics.statistics_dto import StatisticsDTO
from app.services.metrics_service import MetricsService

logger = logging.getLogger(get_config().log_config.logger_name)


class MetricsRoute:
    @staticmethod
    def get_router(metrics_service: MetricsService) -> APIRouter:
        router = APIRouter(tags=['metrics_api'])

        @router.get(
            '/{model_uuid}/reference/statistics',
            status_code=200,
            response_model=StatisticsDTO,
        )
        def get_reference_statistics_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_reference_statistics_by_model_by_uuid(model_uuid)

        @router.get(
            '/{model_uuid}/reference/model-quality',
            status_code=200,
            response_model=ModelQualityDTO,
        )
        def get_reference_model_quality_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_reference_model_quality_by_model_by_uuid(
                model_uuid
            )

        @router.get(
            '/{model_uuid}/reference/data-quality',
            status_code=200,
            response_model=DataQualityDTO,
        )
        def get_reference_data_quality_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_reference_data_quality_by_model_by_uuid(
                model_uuid
            )

        @router.get(
            '/{model_uuid}/current/latest/statistics',
            status_code=200,
            response_model=StatisticsDTO,
        )
        def get_latest_current_statistics_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_current_statistics_by_model_by_uuid(
                model_uuid, None
            )

        @router.get(
            '/{model_uuid}/current/{current_uuid}/statistics',
            status_code=200,
            response_model=StatisticsDTO,
        )
        def get_current_statistics_by_model_by_uuid(
            model_uuid: UUID, current_uuid: UUID
        ):
            return metrics_service.get_current_statistics_by_model_by_uuid(
                model_uuid, current_uuid
            )

        @router.get(
            '/{model_uuid}/current/latest/model-quality',
            status_code=200,
            response_model=ModelQualityDTO,
        )
        def get_latest_current_model_quality_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_current_model_quality_by_model_by_uuid(
                model_uuid, None
            )

        @router.get(
            '/{model_uuid}/current/{current_uuid}/model-quality',
            status_code=200,
            response_model=ModelQualityDTO,
        )
        def get_current_model_quality_by_model_by_uuid(
            model_uuid: UUID, current_uuid: UUID
        ):
            return metrics_service.get_current_model_quality_by_model_by_uuid(
                model_uuid, current_uuid
            )

        @router.get(
            '/{model_uuid}/current/latest/drift',
            status_code=200,
            response_model=DriftDTO,
        )
        def get_latest_current_drift_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_current_drift(model_uuid, None)

        @router.get(
            '/{model_uuid}/current/{current_uuid}/drift',
            status_code=200,
            response_model=DriftDTO,
        )
        def get_current_drift_by_model_by_uuid(model_uuid: UUID, current_uuid: UUID):
            return metrics_service.get_current_drift(model_uuid, current_uuid)

        @router.get(
            '/{model_uuid}/current/latest/data-quality',
            status_code=200,
            response_model=DataQualityDTO,
        )
        def get_latest_current_data_quality_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_current_data_quality_by_model_by_uuid(
                model_uuid, None
            )

        @router.get(
            '/{model_uuid}/current/{current_uuid}/data-quality',
            status_code=200,
            response_model=DataQualityDTO,
        )
        def get_current_data_quality_by_model_by_uuid(
            model_uuid: UUID, current_uuid: UUID
        ):
            return metrics_service.get_current_data_quality_by_model_by_uuid(
                model_uuid, current_uuid
            )

        @router.get(
            '/{model_uuid}/current/latest/percentages',
            status_code=200,
            response_model=PercentagesDTO,
        )
        def get_latest_current_percentages_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_current_percentages_by_model_by_uuid(
                model_uuid, None
            )

        @router.get(
            '/{model_uuid}/current/{current_uuid}/percentages',
            status_code=200,
            response_model=PercentagesDTO,
        )
        def get_current_percentages_by_model_by_uuid(
            model_uuid: UUID, current_uuid: UUID
        ):
            return metrics_service.get_current_percentages_by_model_by_uuid(
                model_uuid, current_uuid
            )

        @router.get(
            '/{model_uuid}/completion/{completion_uuid}/model-quality',
            status_code=200,
            response_model=ModelQualityDTO,
        )
        def get_completion_model_quality_by_model_by_uuid(
            model_uuid: UUID, completion_uuid: UUID
        ):
            return metrics_service.get_completion_model_quality_by_model_by_uuid(
                model_uuid, completion_uuid
            )

        @router.get(
            '/{model_uuid}/reference/embeddings',
            status_code=200,
            response_model=EmbeddingsReportDTO,
        )
        def get_reference_embeddings_by_model_by_uuid(model_uuid: UUID):
            return metrics_service.get_reference_embeddings_by_model_by_uuid(model_uuid)

        @router.get(
            '/{model_uuid}/current/{current_uuid}/embeddings',
            status_code=200,
            response_model=EmbeddingsReportDTO,
        )
        def get_current_embeddings_by_model_by_uuid(model_uuid: UUID, current_uuid: UUID):
            return metrics_service.get_current_embeddings_by_model_by_uuid(model_uuid, current_uuid)

        return router
