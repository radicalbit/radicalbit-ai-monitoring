import unittest
from unittest.mock import MagicMock
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.commons.order_type import OrderType
from app.models.exceptions import (
    ErrorOut,
    ProjectError,
    ProjectInternalError,
    project_exception_handler,
)
from app.models.traces.project_dto import ProjectOut
from app.routes.project_route import ProjectRoute
from app.services.project_service import ProjectService
from tests.commons import db_mock


class ProjectRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_service = MagicMock(spec_set=ProjectService)
        cls.prefix = '/api/projects'

        router = ProjectRoute.get_router(cls.project_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.add_exception_handler(ProjectError, project_exception_handler)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app, raise_server_exceptions=False)

    def test_create_project(self):
        project_in = db_mock.get_sample_project_in()
        project = db_mock.get_sample_project()
        project_out = ProjectOut.from_project(project)
        self.project_service.create_project = MagicMock(return_value=project_out)

        res = self.client.post(
            f'{self.prefix}',
            json=jsonable_encoder(project_in),
        )

        assert res.status_code == 201
        assert jsonable_encoder(project_out) == res.json()
        self.project_service.create_project.assert_called_once_with(project_in)

    def test_exception_handler_model_internal_error(self):
        project_in = db_mock.get_sample_project_in()
        self.project_service.create_project = MagicMock(
            side_effect=ProjectInternalError('error')
        )

        res = self.client.post(
            f'{self.prefix}',
            json=jsonable_encoder(project_in),
        )

        assert res.status_code == 500
        assert jsonable_encoder(ErrorOut('error')) == res.json()
        self.project_service.create_project.assert_called_once_with(project_in)

    def test_get_project_by_uuid(self):
        project = db_mock.get_sample_project()
        project_out = ProjectOut.from_project(project)
        self.project_service.get_project_by_uuid = MagicMock(return_value=project_out)

        res = self.client.get(f'{self.prefix}/{project.uuid}')
        assert res.status_code == 200
        assert jsonable_encoder(project_out) == res.json()
        self.project_service.get_project_by_uuid.assert_called_once_with(project.uuid)

    def test_get_all_projects_paginated(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')

        projects_out = [
            ProjectOut.from_project(project1),
            ProjectOut.from_project(project2),
            ProjectOut.from_project(project3),
        ]
        page = Page.create(items=projects_out, total=len(projects_out), params=Params())
        self.project_service.get_all_projects_paginated = MagicMock(return_value=page)

        res = self.client.get(f'{self.prefix}')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.project_service.get_all_projects_paginated.assert_called_once_with(
            params=Params(page=1, size=50), order=OrderType.ASC, sort=None
        )

    def test_get_all_projects(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')

        projects_out = [
            ProjectOut.from_project(project1),
            ProjectOut.from_project(project2),
            ProjectOut.from_project(project3),
        ]

        self.project_service.get_all_projects = MagicMock(return_value=projects_out)

        res = self.client.get(f'{self.prefix}/all')
        assert res.status_code == 200
        assert jsonable_encoder(projects_out) == res.json()
        self.project_service.get_all_projects.assert_called_once()

    def test_delete_project(self):
        project = db_mock.get_sample_project()
        project_out = ProjectOut.from_project(project)
        self.project_service.delete_project = MagicMock(return_value=project_out)

        res = self.client.delete(f'{self.prefix}/{project.uuid}')
        assert res.status_code == 200
        assert jsonable_encoder(project_out) == res.json()
        self.project_service.delete_project.assert_called_once_with(project.uuid)
