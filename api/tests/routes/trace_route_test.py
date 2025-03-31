from datetime import datetime, timedelta
import unittest
from unittest.mock import MagicMock
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page, Params
from starlette.testclient import TestClient

from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO
from app.models.traces.widget_dto import SessionsTracesDTO, TraceTimeseriesDTO
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

    def test_get_all_sessions(self):
        sessions = db_mock.get_sample_session_tuple()
        sessions_dto = [SessionDTO.model_validate(s) for s in sessions]
        self.trace_service.get_all_sessions = MagicMock(return_value=sessions_dto)
        res = self.client.get(
            f'{self.prefix}/project/{db_mock.PROJECT_UUID}/session/all'
        )
        assert res.status_code == 200
        assert jsonable_encoder(sessions_dto) == res.json()
        self.trace_service.get_all_sessions.assert_called_once_with(
            project_uuid=db_mock.PROJECT_UUID
        )

    def test_get_all_sessions_paginated(self):
        sessions = db_mock.get_sample_session_tuple()
        sessions_dto = [SessionDTO.model_validate(s) for s in sessions]
        page = Page.create(items=sessions_dto, total=len(sessions_dto), params=Params())
        self.trace_service.get_all_sessions_paginated = MagicMock(return_value=page)
        res = self.client.get(f'{self.prefix}/project/{db_mock.PROJECT_UUID}/session')
        assert res.status_code == 200
        assert jsonable_encoder(page) == res.json()
        self.trace_service.get_all_sessions_paginated.assert_called_once_with(
            project_uuid=db_mock.PROJECT_UUID,
            params=Params(page=1, size=50),
            order=OrderType.ASC,
            sort=None,
        )

    def test_get_traces_by_sessions(self):
        session_uuid = uuid.uuid4()
        session_uuid_one = uuid.uuid4()
        from_datetime = datetime.now() - timedelta(hours=1)
        to_datetime = datetime.now()
        session_traces_dto = SessionsTracesDTO.from_row(
            project_uuid=db_mock.PROJECT_UUID,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            rows=[
                db_mock.get_sample_trace_by_session(
                    session_uuid=str(session_uuid), count=10
                ),
                db_mock.get_sample_trace_by_session(
                    session_uuid=str(session_uuid_one), count=4
                ),
            ],
        )
        self.trace_service.get_session_traces_dashboard = MagicMock(
            return_value=session_traces_dto
        )

        res = self.client.get(
            f'{self.prefix}/dashboard/project/{db_mock.PROJECT_UUID}/traces-by-session?fromTimestamp={int(from_datetime.timestamp())}&toTimestamp={int(to_datetime.timestamp())}'
        )
        assert res.status_code == 200
        assert jsonable_encoder(session_traces_dto) == res.json()

    def test_get_trace_time(self):
        traces = db_mock.get_sample_dao_trace_time()
        interval_in_seconds = (
            datetime(year=2025, month=3, day=20, hour=9, minute=0)
            - datetime(year=2025, month=3, day=15, hour=9, minute=0)
        ).total_seconds() / 20
        trace_timeseries_dto = TraceTimeseriesDTO.from_row(
            project_uuid=uuid.UUID(int=0),
            from_datetime=datetime(year=2025, month=3, day=15, hour=9, minute=0),
            to_datetime=datetime(year=2025, month=3, day=20, hour=9, minute=0),
            n=20,
            interval_size_seconds=int(interval_in_seconds),
            rows=traces,
        )
        self.trace_service.get_traces_by_time_dashboard = MagicMock(
            return_value=trace_timeseries_dto
        )
        res = self.client.get(
            f'{self.prefix}/dashboard/project/{str(uuid.UUID(int=0))}/trace_by_time/'
            f'?fromTimestamp={datetime(year=2025, month=3, day=15, hour=9, minute=0).timestamp()}'
            f'&toTimestamp={datetime(year=2025, month=3, day=20, hour=9, minute=0).timestamp()}'
        )
        assert res.status_code == 200
        assert jsonable_encoder(trace_timeseries_dto) == res.json()
        self.trace_service.get_traces_by_time_dashboard.assert_called_once_with(
            uuid.UUID(int=0),
            datetime(year=2025, month=3, day=15, hour=9, minute=0),
            datetime(year=2025, month=3, day=20, hour=9, minute=0),
            15,
        )
