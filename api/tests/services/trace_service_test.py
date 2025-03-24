import datetime
import unittest
from unittest.mock import MagicMock
import uuid

from fastapi_pagination import Page, Params

from app.db.dao.project_dao import ProjectDAO
from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO, TraceDTO
from app.models.traces.widget_dto import SessionsTracesDTO, TraceTimeseriesDTO
from app.services.trace_service import TraceService
from tests.commons import db_mock


class TraceServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace_dao: TraceDAO = MagicMock(spec_set=TraceDAO)
        cls.project_dao: ProjectDAO = MagicMock(spec_set=ProjectDAO)
        cls.trace_service = TraceService(
            trace_dao=cls.trace_dao, project_dao=cls.project_dao
        )
        cls.mocks = [
            cls.trace_dao,
            cls.project_dao,
        ]

    def test_get_all_sessions(self):
        page = Page.create(
            items=db_mock.get_sample_session_tuple(),
            total=len(db_mock.get_sample_session_tuple()),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )
        self.trace_dao.get_all_sessions = MagicMock(return_value=page)
        res = self.trace_service.get_all_sessions(db_mock.PROJECT_UUID)
        assert res.items is not None
        assert len(res.items) == 2
        assert all(isinstance(x, SessionDTO) for x in res.items)

    def test_trace_by_time(self):
        self.trace_dao.get_traces_by_time_dashboard = MagicMock(
            return_value=db_mock.get_sample_dao_trace_time()
        )
        res = self.trace_service.get_traces_by_time_dashboard(
            project_uuid=uuid.UUID(int=0),
            from_datetime=datetime.datetime(
                year=2025, month=3, day=15, hour=9, minute=0
            ),
            to_datetime=datetime.datetime(year=2025, month=3, day=20, hour=9, minute=0),
            n=20,
        )
        assert isinstance(res, TraceTimeseriesDTO)
        assert len(res.traces) == 20
        assert res.traces[8].count == 1
        assert res.traces[8].start_date == datetime.datetime(
            year=2025, month=3, day=17, hour=9, minute=0
        )
        assert res.traces[16].count == 7
        assert res.traces[16].start_date == datetime.datetime(
            year=2025, month=3, day=19, hour=9, minute=0
        )

    def test_interval_size_in_seconds(self):
        interval_size_in_second = self.trace_service._extract_interval(
            from_datetime=datetime.datetime(
                year=2025, month=3, day=15, hour=9, minute=0
            ),
            to_datetime=datetime.datetime(year=2025, month=3, day=15, hour=9, minute=1),
            n=3,
        )
        assert interval_size_in_second == 20

    def test_get_all_root_traces_by_project_uuid(self):
        page = Page.create(
            items=db_mock.get_sample_trace_roots(),
            total=len(db_mock.get_sample_trace_roots()),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )
        self.trace_dao.get_all_root_traces_by_project_uuid = MagicMock(
            return_value=page
        )
        res = self.trace_service.get_all_root_traces_by_project_uuid(
            db_mock.PROJECT_UUID
        )
        assert res.items is not None
        assert len(res.items) == 3
        assert all(isinstance(trace, TraceDTO) for trace in res.items)

    def test_get_trace_by_sessions_dashboard(self):
        session_uuid = uuid.uuid4()
        session_uuid_one = uuid.uuid4()
        self.trace_dao.get_sessions_traces = MagicMock(
            return_value=[
                db_mock.get_sample_trace_by_session(
                    session_uuid=str(session_uuid), count=10
                ),
                db_mock.get_sample_trace_by_session(
                    session_uuid=str(session_uuid_one), count=4
                ),
            ]
        )
        from_datetime = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(
            hours=1
        )
        to_datetime = datetime.datetime.now(tz=datetime.UTC)
        res = self.trace_service.get_session_traces_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
        )
        assert isinstance(res, SessionsTracesDTO)
        assert len(res.traces) == 2
        assert res.project_uuid == db_mock.PROJECT_UUID
        assert res.traces[0].session_uuid == str(session_uuid)
        assert res.traces[0].count == 10
        assert res.traces[1].session_uuid == str(session_uuid_one)
        assert res.traces[1].count == 4
