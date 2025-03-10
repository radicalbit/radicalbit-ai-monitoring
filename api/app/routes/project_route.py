import logging
from uuid import UUID

from fastapi import APIRouter

from app.core import get_config
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

        @router.get('/{project_uuid}', status_code=200, response_model=ProjectOut)
        def get_project_by_uuid(project_uuid: UUID):
            return project_service.get_project_by_uuid(project_uuid)

        return router
