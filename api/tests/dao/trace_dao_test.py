import datetime
import logging
import uuid

from app.core import get_config
from app.db.dao.traces_dao import TraceDAO
from tests.commons import db_mock
from tests.commons.db_integration_ch import DatabaseIntegrationClickhouse

logger = logging.getLogger(get_config().log_config.logger_name)


class TraceDAOTest(DatabaseIntegrationClickhouse):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.trace_dao = TraceDAO(cls.db)

    def test_get_all_sessions(self):
        session_one_uuid = uuid.uuid4()
        session_two_uuid = uuid.uuid4()
        trace_1 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid,
            completion_tokens=11,
            prompt_tokens=536,
        )
        trace_2 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid,
            completion_tokens=25,
            prompt_tokens=555,
        )
        trace_3 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            completion_tokens=34,
            prompt_tokens=810,
        )
        trace_4 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            completion_tokens=28,
            prompt_tokens=859,
        )
        self.insert([trace_1, trace_2, trace_3, trace_4])
        res = self.trace_dao.get_all_sessions(project_uuid=db_mock.PROJECT_UUID)
        assert res is not None
        session_one = [x for x in res if x['session_uuid'] == str(session_one_uuid)]
        session_two = [x for x in res if x['session_uuid'] == str(session_two_uuid)]
        assert session_one[0]['completion_tokens'] == 36
        assert session_two[0]['completion_tokens'] == 62
        assert session_one[0]['prompt_tokens'] == 1091
        assert session_two[0]['prompt_tokens'] == 1669
        assert session_one[0]['total_tokens'] == 1127
        assert session_two[0]['total_tokens'] == 1731

    def test_get_all_sessions_paginated(self):
        session_one_uuid = uuid.uuid4()
        session_two_uuid = uuid.uuid4()
        trace_1 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid,
            completion_tokens=11,
            prompt_tokens=536,
        )
        trace_2 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid,
            completion_tokens=25,
            prompt_tokens=555,
        )
        trace_3 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            completion_tokens=34,
            prompt_tokens=810,
        )
        trace_4 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            completion_tokens=28,
            prompt_tokens=859,
        )
        self.insert([trace_1, trace_2, trace_3, trace_4])
        res = self.trace_dao.get_all_sessions_paginated(
            project_uuid=db_mock.PROJECT_UUID
        )
        assert res.items is not None
        res = [x._mapping for x in res.items]
        session_one = [x for x in res if x['session_uuid'] == str(session_one_uuid)]
        session_two = [x for x in res if x['session_uuid'] == str(session_two_uuid)]
        assert session_one[0]['completion_tokens'] == 36
        assert session_two[0]['completion_tokens'] == 62
        assert session_one[0]['prompt_tokens'] == 1091
        assert session_two[0]['prompt_tokens'] == 1669
        assert session_one[0]['total_tokens'] == 1127
        assert session_two[0]['total_tokens'] == 1731

    def test_get_span_by_id(self):
        trace = db_mock.get_sample_trace()
        self.insert([trace])
        res = self.trace_dao.get_span_by_id(
            project_uuid=db_mock.PROJECT_UUID,
            trace_id=trace.trace_id,
            span_id=trace.span_id,
        )
        assert res.span_id == trace.span_id

    def test_delete_traces_by_project_uuid_trace_id(self):
        trace_one_id = str(uuid.uuid4())
        trace_two_id = str(uuid.uuid4())
        trace_1 = db_mock.get_sample_trace(trace_id=trace_one_id)
        trace_2 = db_mock.get_sample_trace(trace_id=trace_one_id)
        trace_3 = db_mock.get_sample_trace(trace_id=trace_two_id)
        trace_4 = db_mock.get_sample_trace(trace_id=trace_one_id)
        self.insert([trace_1, trace_2, trace_3, trace_4])

        res = self.trace_dao.delete_traces_by_project_uuid_trace_id(
            project_uuid=db_mock.PROJECT_UUID, trace_id=trace_one_id
        )

        assert res == 3

    def test_delete_traces_by_project_uuid_session_uuid(self):
        session_one_uuid = uuid.uuid4()
        session_two_uuid = uuid.uuid4()
        trace_1 = db_mock.get_sample_trace(session_uuid=session_one_uuid)
        trace_2 = db_mock.get_sample_trace(session_uuid=session_two_uuid)
        trace_3 = db_mock.get_sample_trace(session_uuid=session_one_uuid)
        trace_4 = db_mock.get_sample_trace(session_uuid=session_one_uuid)
        self.insert([trace_1, trace_2, trace_3, trace_4])

        res = self.trace_dao.delete_traces_by_project_uuid_session_uuid(
            project_uuid=db_mock.PROJECT_UUID, session_uuid=session_one_uuid
        )

        assert res == 3

    def test_get_all_root_traces_by_project_uuid(self):
        trace_1 = db_mock.get_sample_trace_tree()
        trace_2 = db_mock.get_sample_trace_tree(
            span_id=str(uuid.uuid4()), parent_span_id=db_mock.SPAN_ID
        )
        trace_3 = db_mock.get_sample_trace_tree(
            span_id=str(uuid.uuid4()), parent_span_id=db_mock.SPAN_ID
        )
        self.insert([trace_1, trace_2, trace_3])
        res = self.trace_dao.get_all_root_traces_by_project_uuid(db_mock.PROJECT_UUID)
        assert len(res) == 1
        assert res[0]['trace_id'] == db_mock.TRACE_ID
        assert res[0]['span_id'] == db_mock.SPAN_ID

    def test_get_all_root_traces_by_project_uuid_paginated(self):
        trace_1 = db_mock.get_sample_trace_tree()
        trace_2 = db_mock.get_sample_trace_tree(
            span_id=str(uuid.uuid4()), parent_span_id=db_mock.SPAN_ID
        )
        trace_3 = db_mock.get_sample_trace_tree(
            span_id=str(uuid.uuid4()), parent_span_id=db_mock.SPAN_ID
        )
        self.insert([trace_1, trace_2, trace_3])
        res = self.trace_dao.get_all_root_traces_by_project_uuid_paginated(
            db_mock.PROJECT_UUID
        )
        assert res.items is not None
        traces = [x._mapping for x in res.items]
        assert len(traces) == 1
        assert traces[0]['trace_id'] == db_mock.TRACE_ID
        assert traces[0]['span_id'] == db_mock.SPAN_ID

    def test_get_trace_by_project_uuid_trace_id(self):
        trace_id = db_mock.TRACE_ID
        span_one_id = db_mock.SPAN_ID
        span_two_id = str(uuid.uuid4())
        span_three_id = str(uuid.uuid4())
        trace_1 = db_mock.get_sample_trace_tree(span_id=span_one_id)
        trace_2 = db_mock.get_sample_trace_tree(
            span_id=span_two_id, parent_span_id=span_one_id
        )
        trace_3 = db_mock.get_sample_trace_tree(
            span_id=span_three_id, parent_span_id=span_one_id
        )
        self.insert([trace_1, trace_2, trace_3])
        res = self.trace_dao.get_trace_by_project_uuid_trace_id(
            db_mock.PROJECT_UUID, trace_id=trace_id
        )
        assert res.mappings() is not None
        traces = [dict(trace) for trace in res.mappings()]
        assert len(traces) == 3
        assert traces[0]['trace_id'] == trace_id
        assert traces[0]['span_id'] == span_one_id
        assert traces[1]['trace_id'] == trace_id
        assert traces[1]['span_id'] == span_two_id
        assert traces[2]['trace_id'] == trace_id
        assert traces[2]['span_id'] == span_three_id

    def test_get_latencies_quantiles_for_root_traces_dashboard(self):
        session_one_uuid = uuid.uuid4()
        session_two_uuid = uuid.uuid4()
        trace_1 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid,
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
        trace_2 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid, duration=586108000
        )
        trace_3 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 1, 0, 0, tzinfo=datetime.timezone.utc
            ),
            duration=723863000,
        )
        trace_4 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 2, 0, 0, tzinfo=datetime.timezone.utc
            ),
            duration=631674000,
        )
        self.insert([trace_1, trace_2, trace_3, trace_4])
        from_timestamp = datetime.datetime(
            2025, 3, 12, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        to_timestamp = datetime.datetime(
            2025, 3, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        res = self.trace_dao.get_latencies_quantiles_for_root_traces_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        assert res == (
            str(db_mock.PROJECT_UUID),
            723863000.0,
            1100426200.0,
            1147496600.0,
            1185152920.0,
        )

    def test_get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(self):
        session_one_uuid = uuid.uuid4()
        session_two_uuid = uuid.uuid4()
        trace_1 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid,
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
        trace_2 = db_mock.get_sample_trace(
            session_uuid=session_one_uuid, duration=586108000
        )
        trace_3 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 1, 0, 0, tzinfo=datetime.timezone.utc
            ),
            duration=723863000,
        )
        trace_4 = db_mock.get_sample_trace(
            session_uuid=session_two_uuid,
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 2, 0, 0, tzinfo=datetime.timezone.utc
            ),
            duration=631674000,
        )
        self.insert([trace_1, trace_2, trace_3, trace_4])
        from_timestamp = datetime.datetime(
            2025, 3, 12, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        to_timestamp = datetime.datetime(
            2025, 3, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        res = self.trace_dao.get_latencies_quantiles_for_root_traces_dashboard_by_session_uuid(
            project_uuid=db_mock.PROJECT_UUID,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        quantiles = list(res)
        assert len(quantiles) == 2
        assert (
            str(db_mock.PROJECT_UUID),
            str(session_two_uuid),
            677768500.0,
            714644100.0,
            719253550.0,
            722941110.0,
        ) in quantiles
        assert (
            str(db_mock.PROJECT_UUID),
            str(session_one_uuid),
            1194567000.0,
            1194567000.0,
            1194567000.0,
            1194567000.0,
        ) in quantiles

    def test_get_latencies_quantiles_for_span_leaf_dashboard(self):
        trace_1 = db_mock.get_sample_trace_tree(
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
        trace_2 = db_mock.get_sample_trace_tree(
            span_id=str(uuid.uuid4()),
            parent_span_id=db_mock.SPAN_ID,
            span_name='ChannelWrite<...,agent>.task',
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 0, 8, 0, tzinfo=datetime.timezone.utc
            ),
            duration=732713,
        )
        trace_3 = db_mock.get_sample_trace_tree(
            span_id=str(uuid.uuid4()),
            parent_span_id=db_mock.SPAN_ID,
            span_name='ChannelWrite<...,agent>.task',
            timestamp=datetime.datetime(
                2025, 3, 12, 15, 0, 16, 0, tzinfo=datetime.timezone.utc
            ),
            duration=762634,
        )
        self.insert([trace_1, trace_2, trace_3])
        from_timestamp = datetime.datetime(
            2025, 3, 12, 14, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        to_timestamp = datetime.datetime(
            2025, 3, 12, 16, 0, 0, 0, tzinfo=datetime.timezone.utc
        )
        res = self.trace_dao.get_latencies_quantiles_for_span_leaf_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )
        quantiles = list(res)
        assert len(quantiles) == 1
        assert quantiles[0] == (
            str(db_mock.PROJECT_UUID),
            'ChannelWrite<...,agent>.task',
            747673.5,
            759641.8999999999,
            761137.95,
            762334.79,
        )

    def test_get_traces_by_time_size_15(self):
        trace_one = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_two = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=10,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_three = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_four = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=10,
                tzinfo=datetime.timezone.utc,
            )
        )
        self.insert([trace_one, trace_two, trace_three, trace_four])
        res = self.trace_dao.get_traces_by_time_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_datetime=datetime.datetime(
                year=2025, month=3, day=15, hour=9, minute=0
            ),
            to_datetime=datetime.datetime(year=2025, month=3, day=20, hour=9, minute=0),
            interval_size=1200,
        )
        logger.info('%s', res)
        assert len(res) == 2
        assert res[0]['count'] == 2
        assert res[0]['start_date'] == datetime.datetime(
            year=2025, month=3, day=17, hour=9, minute=0
        )
        assert res[1]['count'] == 2
        assert res[1]['start_date'] == datetime.datetime(
            year=2025, month=3, day=19, hour=10, minute=0
        )

    def test_get_traces_by_time_size_45(self):
        trace_one = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_two = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=45,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_three = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_four = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=45,
                tzinfo=datetime.timezone.utc,
            )
        )
        self.insert([trace_one, trace_two, trace_three, trace_four])
        res = self.trace_dao.get_traces_by_time_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_datetime=datetime.datetime(
                year=2025, month=3, day=15, hour=9, minute=0
            ),
            to_datetime=datetime.datetime(year=2025, month=3, day=20, hour=9, minute=0),
            interval_size=1800,
        )
        assert len(res) == 4
        assert all(i['count'] for i in res) == 1
        assert res[0]['start_date'] == datetime.datetime(
            year=2025, month=3, day=17, hour=9, minute=0
        )
        assert res[1]['start_date'] == datetime.datetime(
            year=2025, month=3, day=17, hour=9, minute=30
        )
        assert res[2]['start_date'] == datetime.datetime(
            year=2025, month=3, day=19, hour=10, minute=0
        )
        assert res[3]['start_date'] == datetime.datetime(
            year=2025, month=3, day=19, hour=10, minute=30
        )

    def test_get_traces_by_time_size_days(self):
        trace_one = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_two = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=45,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_three = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_four = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=45,
                tzinfo=datetime.timezone.utc,
            )
        )
        self.insert([trace_one, trace_two, trace_three, trace_four])
        res = self.trace_dao.get_traces_by_time_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_datetime=datetime.datetime(
                year=2025, month=3, day=15, hour=9, minute=0
            ),
            to_datetime=datetime.datetime(year=2025, month=3, day=20, hour=9, minute=0),
            interval_size=345600,  # four days
        )
        assert len(res) == 1
        assert res[0]['count'] == 4
        assert res[0]['start_date'] == datetime.datetime(
            year=2025, month=3, day=17, hour=9, minute=0
        )

    def test_get_traces_by_time_wrong_timestamp_size(self):
        trace_one = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_two = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=17,
                hour=9,
                minute=10,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_three = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=0,
                tzinfo=datetime.timezone.utc,
            )
        )
        trace_four = db_mock.get_sample_trace(
            timestamp=datetime.datetime(
                year=2025,
                month=3,
                day=19,
                hour=10,
                minute=10,
                tzinfo=datetime.timezone.utc,
            )
        )
        self.insert([trace_one, trace_two, trace_three, trace_four])
        res = self.trace_dao.get_traces_by_time_dashboard(
            project_uuid=db_mock.PROJECT_UUID,
            from_datetime=datetime.datetime(
                year=2025, month=3, day=20, hour=9, minute=0
            ),
            to_datetime=datetime.datetime(year=2025, month=3, day=15, hour=9, minute=0),
            interval_size=1200,
        )
        logger.info('%s', res)
        assert len(res) == 0

    def test_get_trace_by_sessions_dashboard(self):
        session_uuid_one = uuid.uuid4()
        session_uuid_two = uuid.uuid4()
        trace_1 = db_mock.get_sample_trace_tree(session_uuid=session_uuid_one)
        trace_2 = db_mock.get_sample_trace_tree(session_uuid=session_uuid_one)
        trace_3 = db_mock.get_sample_trace_tree(session_uuid=session_uuid_two)
        trace_4 = db_mock.get_sample_trace_tree(session_uuid=session_uuid_two)
        trace_5 = db_mock.get_sample_trace_tree(session_uuid=session_uuid_two)
        self.insert([trace_1, trace_2, trace_3, trace_4, trace_5])
        from_timestamp = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(
            hours=1
        )
        to_timestamp = datetime.datetime.now(tz=datetime.UTC)
        res = self.trace_dao.get_sessions_traces(
            db_mock.PROJECT_UUID, from_timestamp, to_timestamp
        )
        assert len(res) == 2
        assert res[0]['session_uuid'] == str(session_uuid_two)
        assert res[0]['count'] == 3
        assert res[1]['session_uuid'] == str(session_uuid_one)
        assert res[1]['count'] == 2
