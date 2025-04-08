from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.models.commons.order_type import OrderType
from app.models.traces.api_key_dto import ApiKeyIn, ApiKeyOut
from app.services.api_key_service import ApiKeyService


class ApiKeyRoute:
    @staticmethod
    def get_router(api_key_service: ApiKeyService) -> APIRouter:
        router = APIRouter(tags=['api_key_api'])

        @router.post(
            '/project/{project_uuid}', status_code=201, response_model=ApiKeyOut
        )
        def create_api_key(project_uuid: UUID, api_key_in: ApiKeyIn):
            return api_key_service.create_api_key(project_uuid, api_key_in)

        @router.get(
            '/project/{project_uuid}/all',
            status_code=200,
            response_model=list[ApiKeyOut],
        )
        def get_all(project_uuid: UUID):
            return api_key_service.get_all(project_uuid)

        @router.get(
            '/project/{project_uuid}',
            status_code=200,
            response_model=Page[ApiKeyOut],
        )
        def get_all_paginated(
            project_uuid: UUID,
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return api_key_service.get_all_paginated(
                project_uuid, params, _order, _sort
            )

        @router.get(
            '/project/{project_uuid}/api-keys/{api_key_name}',
            status_code=200,
            response_model=ApiKeyOut,
        )
        def get_api_key(project_uuid: UUID, api_key_name: str):
            return api_key_service.get_api_key(project_uuid, api_key_name)

        return router
