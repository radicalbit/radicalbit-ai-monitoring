import logging
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.core import get_config
from app.models.model_dto import ModelIn, ModelOut
from app.models.model_order import OrderType
from app.services.model_service import ModelService

logger = logging.getLogger(get_config().log_config.logger_name)


class ModelRoute:
    @staticmethod
    def get_router(model_service: ModelService) -> APIRouter:
        router = APIRouter(tags=['model_api'])

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

        @router.get('', status_code=200, response_model=Page[ModelOut])
        def get_all_models(
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return model_service.get_all_models(params=params, order=_order, sort=_sort)

        return router
