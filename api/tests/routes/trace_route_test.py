import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO
from app.routes.trace_route import TraceRoute
from app.services.trace_service import TraceService
from tests.commons import db_mock


class TraceRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace_service = MagicMock(spec_set=TraceService)
        cls.prefix = '/api/traces'

        router = TraceRoute.get_router(cls.trace_service)

        app = FastAPI(title='Radicalbit Platform', debug=True)
        app.include_router(router, prefix=cls.prefix)

        cls.client = TestClient(app, raise_server_exceptions=False)

    def test_get_all_projects_paginated(self):
        sessions = db_mock.get_sample_session_tuple()
        sessions_dto = [SessionDTO.model_validate(s) for s in sessions]
        page = Page.create(items=sessions_dto, total=len(sessions_dto), params=Params())
        self.trace_service.get_all_sessions = MagicMock(return_value=page)
        res = self.client.get(f'{self.prefix}/session/all/{db_mock.PROJECT_UUID}')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.trace_service.get_all_sessions.assert_called_once_with(
            project_uuid=db_mock.PROJECT_UUID,
            params=Params(page=1, size=50),
            order=OrderType.ASC,
            sort=None,
        )
