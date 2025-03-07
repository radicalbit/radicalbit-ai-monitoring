import logging

from fastapi import APIRouter
from models.traces.project_dto import ProjectIn, ProjectOut
from services.project_service import ProjectService

from app.core import get_config

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

        return router
