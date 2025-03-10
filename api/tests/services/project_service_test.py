import unittest
from unittest.mock import MagicMock

import pytest

from app.db.dao.project_dao import ProjectDAO
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


project_uuid = db_mock.PROJECT_UUID
