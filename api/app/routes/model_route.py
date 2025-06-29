import logging
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Response
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.core import get_config
from app.models.alert_dto import AlertDTO
from app.models.commons.order_type import OrderType
from app.models.metrics.tot_percentages_dto import TotPercentagesDTO
from app.models.model_dto import ModelFeatures, ModelFeaturesFE, ModelIn, ModelOut
from app.services.model_service import ModelService

logger = logging.getLogger(get_config().log_config.logger_name)


class ModelRoute:
    @staticmethod
    def get_router(model_service: ModelService) -> APIRouter:
        router = APIRouter(tags=['model_api'])

        @router.get('', status_code=200, response_model=Page[ModelOut])
        def get_all_models_paginated(
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return model_service.get_all_models_paginated(
                params=params, order=_order, sort=_sort
            )

        @router.get('/all', status_code=200, response_model=List[ModelOut])
        def get_all_models():
            return model_service.get_all_models()

        @router.get('/last_n', status_code=200, response_model=List[ModelOut])
        def get_last_n_models(n_models: int):
            return model_service.get_last_n_models_percentages(n_models)

        @router.get('/last_n_alerts', status_code=200, response_model=List[AlertDTO])
        def get_last_n_alerts(n_alerts: int):
            return model_service.get_last_n_alerts(n_alerts)

        @router.get(
            '/tot_percentages', status_code=200, response_model=TotPercentagesDTO
        )
        def get_tot_percentages():
            return model_service.get_summarized_percentages()

        @router.post('', status_code=201, response_model=ModelOut)
        def create_model(model_in: ModelIn):
            model = model_service.create_model(model_in)
            logger.info('Model %s with name %s created.', model.uuid, model.name)
            return model

        @router.get('/{model_uuid}', status_code=200, response_model=ModelOut)
        def get_model_by_uuid(model_uuid: UUID):
            return model_service.get_model_by_uuid(model_uuid)

        @router.delete('/{model_uuid}', status_code=200, response_model=ModelOut)
        def delete_model(model_uuid: UUID):
            model = model_service.delete_model(model_uuid)
            logger.info('Model %s with name %s deleted.', model.uuid, model.name)
            return model

        @router.patch('/{model_uuid}/update-features', status_code=200)
        def update_model_features_by_uuid(
            model_uuid: UUID, model_features: ModelFeatures
        ):
            if model_service.update_model_features_by_uuid(model_uuid, model_features):
                return Response(status_code=200)
            return Response(status_code=400)

        @router.patch('/{model_uuid}/update-features-default', status_code=200)
        def update_model_features_default_by_uuid(
            model_uuid: UUID, model_features: ModelFeaturesFE
        ):
            default_drift_features = model_features.to_model_features_default()
            if model_service.update_model_features_by_uuid(
                model_uuid, default_drift_features
            ):
                return Response(status_code=200)
            return Response(status_code=400)

        return router
