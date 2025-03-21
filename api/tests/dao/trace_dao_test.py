import datetime
import logging
import uuid

from app.core import get_config
from app.db.dao.traces_dao import TraceDAO
from tests.commons.db_integration_ch import DatabaseIntegrationClickhouse
from tests.commons.db_mock import (
    SESSION_UUID,
    SESSION_UUID_TWO,
    get_sample_session,
    get_sample_session_tree,
)

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

    def test_get_all_root_traces_by_project_uuid(self):
        self.insert(get_sample_session_tree())
        res = self.trace_dao.get_all_root_traces_by_project_uuid(uuid.UUID(int=0))
        assert res.items is not None
        traces = [x._mapping for x in res.items]
        assert len(traces) == 1
        assert traces[0]['trace_id'] == '61631e0e43fd5cdf9b4b855462d83452'
        assert traces[0]['span_id'] == 'dd250200569ce295'
        assert traces[0]['completion_tokens'] == 30
        assert traces[0]['prompt_tokens'] == 1000
        assert traces[0]['total_tokens'] == 1030
        assert traces[0]['number_of_errors'] == 1

    def test_get_trace_by_project_uuid_trace_id(self):
        self.insert(get_sample_session_tree())
        res = self.trace_dao.get_trace_by_project_uuid_trace_id(
            uuid.UUID(int=0), trace_id='61631e0e43fd5cdf9b4b855462d83452'
        )
        assert res.mappings() is not None
        traces = [dict(trace) for trace in res.mappings()]
        assert len(traces) == 3
        assert traces[0]['trace_id'] == '61631e0e43fd5cdf9b4b855462d83452'
        assert traces[0]['span_id'] == 'dd250200569ce295'
        assert traces[1]['trace_id'] == '61631e0e43fd5cdf9b4b855462d83452'
        assert traces[1]['span_id'] == '6fd4061cad7dd30d'
        assert traces[2]['trace_id'] == '61631e0e43fd5cdf9b4b855462d83452'
        assert traces[2]['span_id'] == '731fa4f1f5068187'

    def test_get_latencies_quantiles_for_root_traces_dashboard(self):
        self.insert(get_sample_session())
        from_timestamp = datetime.datetime(
            2025, 3, 12, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        to_timestamp = datetime.datetime(
            2025, 3, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        res = self.trace_dao.get_latencies_quantiles_for_root_traces_dashboard(
            project_uuid=uuid.UUID(int=0),
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        assert res == (
            '00000000-0000-0000-0000-000000000000',
            723863000.0,
            1100426200.0,
            1147496600.0,
            1185152920.0,
        )

    def test_get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(self):
        self.insert(get_sample_session())
        from_timestamp = datetime.datetime(
            2025, 3, 12, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        to_timestamp = datetime.datetime(
            2025, 3, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        res = self.trace_dao.get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
            project_uuid=uuid.UUID(int=0),
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        quantiles = list(res)
        assert len(quantiles) == 2
        assert quantiles[0] == (
            '00000000-0000-0000-0000-000000000000',
            '286751f8-398c-4a8c-898f-78caf9453fde',
            677768500.0,
            714644100.0,
            719253550.0,
            722941110.0,
        )
        assert quantiles[1] == (
            '00000000-0000-0000-0000-000000000000',
            'a8dd1f4d-d076-4035-99e2-443c550c71a4',
            1194567000.0,
            1194567000.0,
            1194567000.0,
            1194567000.0,
        )

    def test_get_latencies_quantiles_for_span_leaf_dashboard(self):
        self.insert(get_sample_session_tree())
        from_timestamp = datetime.datetime(
            2025, 3, 12, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        to_timestamp = datetime.datetime(
            2025, 3, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        res = self.trace_dao.get_latencies_quantiles_for_span_leaf_dashboard(
            project_uuid=uuid.UUID(int=0),
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        quantiles = list(res)
        assert len(quantiles) == 1
        assert quantiles[0] == (
            '00000000-0000-0000-0000-000000000000',
            'ChannelWrite<...,agent>.task',
            747673.5,
            759641.8999999999,
            761137.95,
            762334.79,
        )
