from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.project_dao import ProjectDAO
from app.models.commons.order_type import OrderType
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

    def get_all_projects(self) -> List[ProjectOut]:
        projects = self.project_dao.get_all()
        # TODO: add query to clickhouse to retrieve project trace number
        return [ProjectOut.from_project(project, traces=None) for project in projects]

    def get_all_projects_paginated(
        self,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ProjectOut]:
        projects = self.project_dao.get_all_paginated(
            params=params,
            order=order,
            sort=sort,
        )
        # TODO: add query to clickhouse to retrieve project trace number
        projects_out = [
            ProjectOut.from_project(project, traces=None) for project in projects.items
        ]
        return Page.create(
            items=projects_out,
            params=params,
            total=projects.total,
        )
