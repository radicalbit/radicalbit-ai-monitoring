import copy
import unittest
from unittest.mock import MagicMock
import uuid

from fastapi_pagination import Page, Params
import pytest

from app.db.dao.project_dao import ProjectDAO
from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.exceptions import ProjectNotFoundError
from app.models.traces.project_dto import ProjectOut
from app.services.api_key_security import ApiKeySecurity
from app.services.project_service import ProjectService
from tests.commons import db_mock


class ProjectServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_dao: ProjectDAO = MagicMock(spec_set=ProjectDAO)
        cls.trace_dao: TraceDAO = MagicMock(spec_set=TraceDAO)
        cls.api_key_security: ApiKeySecurity = MagicMock(spec_set=ApiKeySecurity)
        cls.project_service = ProjectService(
            project_dao=cls.project_dao,
            trace_dao=cls.trace_dao,
            api_key_security=cls.api_key_security,
        )
        cls.mocks = [
            cls.project_dao,
            cls.trace_dao,
        ]

    def test_create_project_ok(self):
        project = db_mock.get_sample_project()
        api_key_sec = db_mock.get_sample_api_key_sec()
        self.project_dao.insert = MagicMock(return_value=project)
        self.api_key_security.generate_key = MagicMock(return_value=api_key_sec)
        project_in = db_mock.get_sample_project_in()
        res = self.project_service.create_project(project_in)
        self.project_dao.insert.assert_called_once()
        assert res == ProjectOut.from_project(
            project=project, plain_api_key=db_mock.PLAIN_KEY
        )

    def test_get_project_by_uuid_ok(self):
        project = db_mock.get_sample_project()
        traces = 5
        self.project_dao.get_by_uuid = MagicMock(return_value=project)
        self.trace_dao.count_distinct_traces_by_project_uuid = MagicMock(
            return_value=traces
        )
        res = self.project_service.get_project_by_uuid(project.uuid)
        self.project_dao.get_by_uuid.assert_called_once()
        self.trace_dao.count_distinct_traces_by_project_uuid.assert_called_once()

        assert res == ProjectOut.from_project(project=project, traces=traces)

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

        traces = 5

        projects_out = [
            ProjectOut.from_project(project=project1, traces=traces),
            ProjectOut.from_project(project=project2, traces=traces),
            ProjectOut.from_project(project=project3, traces=traces),
        ]
        page = Page.create(
            items=projects_out,
            total=len(projects_out),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )

        self.project_dao.get_all_paginated = MagicMock(return_value=page)
        self.trace_dao.count_distinct_traces_by_project_uuid = MagicMock(
            return_value=traces
        )

        result = self.project_service.get_all_projects_paginated(
            params=Params(page=1, size=10), order=OrderType.ASC, sort=None
        )

        self.project_dao.get_all_paginated.assert_called_once_with(
            params=Params(page=1, size=10), order=OrderType.ASC, sort=None
        )
        self.trace_dao.count_distinct_traces_by_project_uuid.assert_called()

        assert result.total == 3
        assert len(result.items) == 3
        assert result.items[0].name == 'project1'
        assert result.items[0].traces == traces
        assert result.items[1].name == 'project2'
        assert result.items[1].traces == traces
        assert result.items[2].name == 'project3'
        assert result.items[2].traces == traces

    def test_get_all_projects_ok(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')

        projects = [project1, project2, project3]

        traces = 5

        self.project_dao.get_all = MagicMock(return_value=projects)
        self.trace_dao.count_distinct_traces_by_project_uuid = MagicMock(
            return_value=traces
        )

        result = self.project_service.get_all_projects()

        self.project_dao.get_all.assert_called_once()
        self.trace_dao.count_distinct_traces_by_project_uuid.assert_called()

        assert len(result) == 3
        assert result[0].name == 'project1'
        assert result[0].traces == traces
        assert result[1].name == 'project2'
        assert result[1].traces == traces
        assert result[2].name == 'project3'
        assert result[2].traces == traces

    def test_update_project_ok(self):
        project = db_mock.get_sample_project()
        traces = 5
        self.project_dao.get_by_uuid = MagicMock(return_value=project)
        self.trace_dao.count_distinct_traces_by_project_uuid = MagicMock(
            return_value=traces
        )
        self.project_dao.update = MagicMock(return_value=1)
        to_update = copy.deepcopy(project)
        to_update.name = 'new_project_name'
        self.project_dao.get_by_uuid = MagicMock(return_value=to_update)
        project_in = db_mock.get_sample_project_in(name=to_update.name)
        res = self.project_service.update_project(project_in, project.uuid)
        self.project_dao.get_by_uuid.assert_called_with(project.uuid)
        self.trace_dao.count_distinct_traces_by_project_uuid.assert_called_once_with(
            project.uuid
        )
        self.project_dao.update.assert_called_once_with(to_update)

        assert res == ProjectOut.from_project(project=to_update, traces=traces)

    def test_delete_project_ok(self):
        project = db_mock.get_sample_project()
        traces = 5
        self.project_dao.get_by_uuid = MagicMock(return_value=project)
        self.trace_dao.count_distinct_traces_by_project_uuid = MagicMock(
            return_value=traces
        )
        self.project_dao.delete = MagicMock(return_value=1)
        res = self.project_service.delete_project(project_uuid)
        self.project_dao.get_by_uuid.assert_called_once_with(project.uuid)
        self.trace_dao.count_distinct_traces_by_project_uuid.assert_called_once_with(
            project.uuid
        )
        self.project_dao.delete.assert_called_once_with(project.uuid)

        assert res == ProjectOut.from_project(project=project, traces=traces)


project_uuid = db_mock.PROJECT_UUID
