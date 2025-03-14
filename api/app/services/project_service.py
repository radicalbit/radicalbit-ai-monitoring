from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params

from app.db.dao.project_dao import ProjectDAO
from app.db.dao.traces_dao import TraceDAO
from app.db.tables.project_table import Project
from app.models.commons.order_type import OrderType
from app.models.exceptions import ProjectInternalError, ProjectNotFoundError
from app.models.traces.project_dto import ProjectIn, ProjectOut


class ProjectService:
    def __init__(
        self,
        project_dao: ProjectDAO,
        trace_dao: TraceDAO,
    ):
        self.project_dao = project_dao
        self.trace_dao = trace_dao

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
        project = self._check_and_get_project(project_uuid)
        traces = self.trace_dao.count_distinct_traces_by_project_uuid(project_uuid)
        return ProjectOut.from_project(project, traces)

    def get_all_projects(self) -> List[ProjectOut]:
        projects = self.project_dao.get_all()

        projects_out = []
        for project in projects:
            traces = self.trace_dao.count_distinct_traces_by_project_uuid(project.uuid)
            projects_out.append(ProjectOut.from_project(project, traces))

        return projects_out

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

        projects_out = []
        for project in projects.items:
            traces = self.trace_dao.count_distinct_traces_by_project_uuid(project.uuid)
            projects_out.append(ProjectOut.from_project(project, traces))

        return Page.create(
            items=projects_out,
            params=params,
            total=projects.total,
        )

    def delete_project(self, project_uuid: UUID) -> Optional[ProjectOut]:
        project = self._check_and_get_project(project_uuid)
        traces = self.trace_dao.count_distinct_traces_by_project_uuid(project_uuid)
        self.project_dao.delete(project_uuid)
        return ProjectOut.from_project(project, traces)

    def _check_and_get_project(self, project_uuid: UUID) -> Project:
        project = self.project_dao.get_by_uuid(project_uuid)
        if not project:
            raise ProjectNotFoundError(f'Project {project_uuid} not found')
        return project
