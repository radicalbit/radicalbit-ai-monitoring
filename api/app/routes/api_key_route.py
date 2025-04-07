from uuid import UUID

from fastapi import APIRouter

from app.models.traces.api_key_dto import ApiKeyIn, ApiKeyOut
from app.services.api_key_service import ApiKeyService


class ApiKeyRoute:
    @staticmethod
    def get_router(api_key_service: ApiKeyService) -> APIRouter:
        router = APIRouter(tags=['api_key_api'])

        @router.post(
            '/project/{project_uuid}/', status_code=201, response_model=ApiKeyOut
        )
        def create_api_key(project_uuid: UUID, api_key_in: ApiKeyIn):
            return api_key_service.create_api_key(project_uuid, api_key_in)

        return router
