import logging
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Query
from fastapi_pagination import Page, Params

from app.core import get_config
from app.models.commons.order_type import OrderType
from app.models.traces.project_dto import ProjectIn, ProjectOut
from app.services.project_service import ProjectService

logger = logging.getLogger(get_config().log_config.logger_name)


class ProjectRoute:
    @staticmethod
    def get_router(project_service: ProjectService) -> APIRouter:
        router = APIRouter(tags=['project_api'])

        @router.post('', status_code=201, response_model=ProjectOut)
        def create_project(project_in: ProjectIn):
            project = project_service.create_project(project_in)
            logger.info('Project %s with name %s created.', project.uuid, project.name)
            return project

        @router.get('/all', status_code=200, response_model=List[ProjectOut])
        def get_all_projects():
            return project_service.get_all_projects()

        @router.get('/{project_uuid}', status_code=200, response_model=ProjectOut)
        def get_project_by_uuid(project_uuid: UUID):
            return project_service.get_project_by_uuid(project_uuid)

        @router.get('', status_code=200, response_model=Page[ProjectOut])
        def get_all_projects_paginated(
            _page: Annotated[int, Query()] = 1,
            _limit: Annotated[int, Query()] = 50,
            _order: Annotated[OrderType, Query()] = OrderType.ASC,
            _sort: Annotated[Optional[str], Query()] = None,
        ):
            params = Params(page=_page, size=_limit)
            return project_service.get_all_projects_paginated(
                params=params, order=_order, sort=_sort
            )

        @router.delete('/{project_uuid}', status_code=200, response_model=ProjectOut)
        def delete_project(project_uuid: UUID):
            project = project_service.delete_project(project_uuid)
            logger.info('Project %s with name %s deleted.', project.uuid, project.name)
            return project

        return router
