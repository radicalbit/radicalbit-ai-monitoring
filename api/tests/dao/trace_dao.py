from app.db.dao.traces_dao import TraceDAO
from tests.commons.db_integration_ch import DatabaseIntegrationCh


class TraceDAOTest(DatabaseIntegrationCh):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.trace_dao = TraceDAO(cls.ch_db)

    def test_get_by_uuid(self):
        pass
