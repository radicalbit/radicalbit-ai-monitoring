import unittest
from unittest.mock import MagicMock

from db.dao.project_dao import ProjectDAO
from models.traces.project_dto import ProjectOut
from services.project_service import ProjectService

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
