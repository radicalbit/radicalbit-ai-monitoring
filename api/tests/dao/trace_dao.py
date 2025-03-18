import logging
import uuid

from app.core import get_config
from app.db.dao.traces_dao import TraceDAO
from tests.commons.db_integration_ch import DatabaseIntegrationClickhouse
from tests.commons.db_mock import SESSION_UUID, SESSION_UUID_TWO, get_sample_session

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceDAOTest(DatabaseIntegrationClickhouse):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.trace_dao = TraceDAO(cls.db)

    def test_get_all_sessions(self):
        self.insert(get_sample_session())
        res = self.trace_dao.get_all_sessions(uuid.UUID(int=0))
        assert res.items is not None
        res = [x._mapping for x in res.items]
        session_one = [x for x in res if x['session_uuid'] == str(SESSION_UUID)]
        session_two = [x for x in res if x['session_uuid'] == str(SESSION_UUID_TWO)]
        assert session_one[0]['completion_tokens'] == 36
        assert session_two[0]['completion_tokens'] == 62
        assert session_one[0]['prompt_tokens'] == 1091
        assert session_two[0]['prompt_tokens'] == 1669
        assert session_one[0]['total_tokens'] == 1127
        assert session_two[0]['total_tokens'] == 1731
        self.clean()
