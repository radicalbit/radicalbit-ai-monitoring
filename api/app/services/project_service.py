from uuid import UUID

from app.db.dao.project_dao import ProjectDAO
from app.models.exceptions import ProjectInternalError, ProjectNotFoundError
from app.models.traces.project_dto import ProjectIn, ProjectOut


class ProjectService:
    def __init__(
        self,
        project_dao: ProjectDAO,
    ):
        self.project_dao = project_dao

    def create_project(self, project_in: ProjectIn) -> ProjectOut:
        try:
            to_insert = project_in.to_project()
            inserted = self.project_dao.insert(to_insert)
            return ProjectOut.from_project(inserted)
        except Exception as e:
            raise ProjectInternalError(
                f'An error occurred while creating the project: {e}'
            ) from e

    def get_project_by_uuid(self, project_uuid: UUID) -> ProjectOut:
        project = self.project_dao.get_by_uuid(project_uuid)
        if not project:
            raise ProjectNotFoundError(f'Project {project_uuid} not found')
        # TODO: add query to clickhouse to retrieve project trace number
        return ProjectOut.from_project(project, traces=None)
