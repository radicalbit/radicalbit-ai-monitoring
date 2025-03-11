import unittest
from unittest.mock import MagicMock
import uuid

from fastapi_pagination import Page, Params
import pytest

from app.db.dao.project_dao import ProjectDAO
from app.models.commons.order_type import OrderType
from app.models.exceptions import ProjectNotFoundError
from app.models.traces.project_dto import ProjectOut
from app.services.project_service import ProjectService
from tests.commons import db_mock


class ProjectServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_dao: ProjectDAO = MagicMock(spec_set=ProjectDAO)
        cls.project_service = ProjectService(
            project_dao=cls.project_dao,
        )
        cls.mocks = [
            cls.project_dao,
        ]

    def test_create_project_ok(self):
        project = db_mock.get_sample_project()
        self.project_dao.insert = MagicMock(return_value=project)
        project_in = db_mock.get_sample_project_in()
        res = self.project_service.create_project(project_in)
        self.project_dao.insert.assert_called_once()

        assert res == ProjectOut.from_project(project)

    def test_get_project_by_uuid_ok(self):
        project = db_mock.get_sample_project()
        self.project_dao.get_by_uuid = MagicMock(return_value=project)
        res = self.project_service.get_project_by_uuid(project.uuid)
        self.project_dao.get_by_uuid.assert_called_once()

        assert res == ProjectOut.from_project(project, traces=None)

    def test_get_project_by_uuid_not_found(self):
        self.project_dao.get_by_uuid = MagicMock(return_value=None)
        pytest.raises(
            ProjectNotFoundError, self.project_service.get_project_by_uuid, project_uuid
        )
        self.project_dao.get_by_uuid.assert_called_once()

    def test_get_all_projects_paginated_ok(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')

        projects_out = [
            ProjectOut.from_project(project1),
            ProjectOut.from_project(project2),
            ProjectOut.from_project(project3),
        ]
        page = Page.create(
            items=projects_out,
            total=len(projects_out),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )

        self.project_dao.get_all_paginated = MagicMock(return_value=page)

        result = self.project_service.get_all_projects_paginated(
            params=Params(page=1, size=10), order=OrderType.ASC, sort=None
        )

        self.project_dao.get_all_paginated.assert_called_once_with(
            params=Params(page=1, size=10), order=OrderType.ASC, sort=None
        )

        assert result.total == 3
        assert len(result.items) == 3
        assert result.items[0].name == 'project1'
        assert result.items[1].name == 'project2'
        assert result.items[2].name == 'project3'

    def test_get_all_projects_ok(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')

        projects = [project1, project2, project3]

        self.project_dao.get_all = MagicMock(return_value=projects)

        result = self.project_service.get_all_projects()

        self.project_dao.get_all.assert_called_once()

        assert len(result) == 3
        assert result[0].name == 'project1'
        assert result[1].name == 'project2'
        assert result[2].name == 'project3'


project_uuid = db_mock.PROJECT_UUID
