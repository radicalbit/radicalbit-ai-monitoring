from app.db.dao.traces_dao import TraceDAO
from tests.commons import db_mock
from tests.commons.db_integration_ch import DatabaseIntegrationCh


class TraceDAOTest(DatabaseIntegrationCh):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.trace_dao = TraceDAO(cls.ch_db)

    def test_get_by_uuid(self):
        session = db_mock.get_sample_session()
        inserted = [self.insert(t) for t in session]
        print(inserted)
        retrieved = self.trace_dao.get_all_sessions()
        # # assert retrieved
