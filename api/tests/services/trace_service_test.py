import unittest
from unittest.mock import MagicMock

from fastapi_pagination import Page, Params

from app.db.dao.project_dao import ProjectDAO
from app.db.dao.traces_dao import TraceDAO
from app.models.commons.order_type import OrderType
from app.models.traces.tracing_dto import SessionDTO, TraceDTO
from app.services.trace_service import TraceService
from tests.commons.db_mock import (
    SERVICE_NAME,
    get_sample_session_tuple,
    get_sample_trace_roots,
)


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
            items=get_sample_session_tuple(),
            total=len(get_sample_session_tuple()),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )
        self.trace_dao.get_all_sessions = MagicMock(return_value=page)
        res = self.trace_service.get_all_sessions(SERVICE_NAME)
        assert res.items is not None
        assert len(res.items) == 2
        assert all(isinstance(x, SessionDTO) for x in res.items)

    def test_get_all_root_traces_by_project_uuid(self):
        page = Page.create(
            items=get_sample_trace_roots(),
            total=len(get_sample_trace_roots()),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )
        self.trace_dao.get_all_root_traces_by_project_uuid = MagicMock(
            return_value=page
        )
        res = self.trace_service.get_all_root_traces_by_project_uuid(SERVICE_NAME)
        assert res.items is not None
        assert len(res.items) == 3
        assert all(isinstance(trace, TraceDTO) for trace in res.items)
