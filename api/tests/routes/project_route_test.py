import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from models.traces.project_dto import ProjectOut
from routes.project_route import ProjectRoute
from services.project_service import ProjectService
from starlette.testclient import TestClient

from app.models.exceptions import (
    ErrorOut,
    ProjectError,
    ProjectInternalError,
    project_exception_handler,
)
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
