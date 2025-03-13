import unittest
from unittest.mock import MagicMock

from app.db.dao.traces_dao import TraceDAO
from app.services.trace_service import TraceService


class TraceServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace_dao: TraceDAO = MagicMock(spec_set=TraceDAO)
        cls.trace_service = TraceService(
            trace_dao=cls.trace_dao,
        )
        cls.mocks = [
            cls.trace_dao,
        ]

    def test_get_all_sessions(self):
        pass
