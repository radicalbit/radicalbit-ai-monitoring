import logging
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from sqlalchemy.exc import IntegrityError

from app.core import get_config
from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.project_dao import ProjectDAO
from app.models.commons.order_type import OrderType
from app.models.exceptions import (
    ApiKeyInternalError,
    ApiKeyNotFoundError,
    ExistingApiKeyError,
    ProjectNotFoundError,
)
from app.models.traces.api_key_dto import ApiKeyIn, ApiKeyOut
from app.services.api_key_security import ApiKeySecurity

logger = logging.getLogger(get_config().log_config.logger_name)


class ApiKeyService:
    def __init__(
        self,
        api_key_dao: ApiKeyDAO,
        project_dao: ProjectDAO,
        api_key_security: ApiKeySecurity,
    ):
        self.api_key_dao = api_key_dao
        self.project_dao = project_dao
        self.api_key_security = api_key_security

    def _check_project(self, project_uuid: UUID):
        project = self.project_dao.get_by_uuid(project_uuid)
        if not project:
            raise ProjectNotFoundError(f'Project {project_uuid} not found')

    def create_api_key(self, project_uuid: UUID, api_key_in: ApiKeyIn) -> ApiKeyOut:
        self._check_project(project_uuid)
        api_key_sec = self.api_key_security.generate_key()
        to_insert = api_key_in.to_api_key(
            project_uuid=project_uuid,
            hashed_key=api_key_sec.hashed_key,
            obscured_key=api_key_sec.obscured_key,
        )
        try:
            inserted = self.api_key_dao.insert(to_insert)
        except IntegrityError as exc:
            raise ExistingApiKeyError(
                f'A key with name {api_key_in.name} already exists in project {project_uuid}'
            ) from exc
        except Exception as exc:
            raise ApiKeyInternalError(
                f'An error occurred while creating the api_key: {exc}'
            ) from exc

        return ApiKeyOut.from_api_key(inserted, api_key_sec.plain_key, project_uuid)

    def get_all(self, project_uuid: UUID) -> list[ApiKeyOut]:
        self._check_project(project_uuid=project_uuid)
        api_keys = self.api_key_dao.get_all(project_uuid=project_uuid)
        return [ApiKeyOut.from_api_key_obscured(i, project_uuid) for i in api_keys]

    def get_all_paginated(
        self,
        project_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ApiKeyOut]:
        self._check_project(project_uuid=project_uuid)
        api_keys = self.api_key_dao.get_all_paginated(
            project_uuid=project_uuid, params=params, order=order, sort=sort
        )
        return Page.create(
            items=[
                ApiKeyOut.from_api_key_obscured(i, project_uuid) for i in api_keys.items
            ],
            params=params,
            total=api_keys.total,
        )

    def get_api_key(self, project_uuid: UUID, name: str) -> ApiKeyOut:
        self._check_project(project_uuid=project_uuid)
        api_key = self.api_key_dao.get_api_key(project_uuid, name)
        if not api_key:
            raise ApiKeyNotFoundError(f'ApiKey {name} not found')
        return ApiKeyOut.from_api_key_obscured(api_key, project_uuid)
