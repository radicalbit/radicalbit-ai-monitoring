import unittest
import uuid

import responses

from radicalbit_platform_sdk.apis import TracingDashboard
from radicalbit_platform_sdk.models import (
    LatenciesWidget,
    SessionsTraces,
    TraceTimeseries,
)


class TracingDashboardTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://api:9000'
        self.project_uuid = uuid.uuid4()
        self.dashboard = TracingDashboard(self.base_url, self.project_uuid)

        self.from_timestamp = 1700000000
        self.to_timestamp = 1700001000

    @responses.activate
    def test_get_latencies_quantiles_for_root_traces_ok(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/root_latencies?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=200,
            json={
                'projectUuid': str(self.project_uuid),
                'p50_ms': 1.0,
                'p90_ms': 2.0,
                'p95_ms': 3.0,
                'p99_ms': 3.0,
            },
        )

        result = self.dashboard.get_latencies_quantiles_for_root_traces(
            self.from_timestamp, self.to_timestamp
        )
        assert isinstance(result, LatenciesWidget)
        assert result.p50_ms == 1.0
        assert result.p99_ms == 3.0

    @responses.activate
    def test_get_latencies_quantiles_for_root_traces_no_content(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/root_latencies?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=204,
        )

        result = self.dashboard.get_latencies_quantiles_for_root_traces(
            self.from_timestamp, self.to_timestamp
        )
        assert result is None

    @responses.activate
    def test_get_latencies_quantiles_for_root_traces_by_session_uuid_ok(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/root_latencies_session?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=200,
            json=[
                {
                    'projectUuid': str(self.project_uuid),
                    'p50_ms': 1.0,
                    'p90_ms': 2.0,
                    'p95_ms': 2.5,
                    'p99_ms': 3.0,
                },
                {
                    'projectUuid': str(self.project_uuid),
                    'p50_ms': 2.0,
                    'p90_ms': 3.0,
                    'p95_ms': 3.5,
                    'p99_ms': 4.0,
                },
            ],
        )

        result = self.dashboard.get_latencies_quantiles_for_root_traces_by_session_uuid(
            self.from_timestamp, self.to_timestamp
        )
        assert isinstance(result, list)
        assert isinstance(result[0], LatenciesWidget)
        assert isinstance(result[1], LatenciesWidget)
        assert result[0].p50_ms == 1.0
        assert result[1].p90_ms == 3.0

    @responses.activate
    def test_get_latencies_quantiles_for_span_leaf_ok(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/leaf_latencies?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=200,
            json=[
                {
                    'projectUuid': str(self.project_uuid),
                    'p50_ms': 0.5,
                    'p90_ms': 1.5,
                    'p95_ms': 2.0,
                    'p99_ms': 2.5,
                }
            ],
        )

        result = self.dashboard.get_latencies_quantiles_for_span_leaf(
            self.from_timestamp, self.to_timestamp
        )
        assert isinstance(result, list)
        assert isinstance(result[0], LatenciesWidget)
        assert result[0].p50_ms == 0.5

    @responses.activate
    def test_get_traces_by_time_ok(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/trace_by_time?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=200,
            json={
                'projectUuid': str(self.project_uuid),
                'fromDatetime': '2023-10-10T00:00:00',
                'toDatetime': '2023-10-10T01:00:00',
                'n': 15,
                'traces': [{'count': 5, 'startDate': '2023-10-10T00:10:00'}],
            },
        )

        result = self.dashboard.get_traces_by_time(
            self.from_timestamp, self.to_timestamp
        )
        assert isinstance(result, TraceTimeseries)
        assert result.n == 15
        assert result.traces[0].count == 5

    @responses.activate
    def test_get_traces_by_time_no_content(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/trace_by_time?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=204,
        )

        result = self.dashboard.get_traces_by_time(
            self.from_timestamp, self.to_timestamp
        )
        assert result is None

    @responses.activate
    def test_get_sessions_traces_ok(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/traces-by-session?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=200,
            json={
                'projectUuid': str(self.project_uuid),
                'fromDatetime': '2023-10-10T00:00:00',
                'toDatetime': '2023-10-10T01:00:00',
                'traces': [{'count': 7, 'sessionUuid': str(uuid.uuid4())}],
            },
        )

        result = self.dashboard.get_sessions_traces(
            self.from_timestamp, self.to_timestamp
        )
        assert isinstance(result, SessionsTraces)
        assert result.traces[0].count == 7

    @responses.activate
    def test_get_sessions_traces_no_content(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/dashboard/project/{self.project_uuid}/traces-by-session?fromTimestamp={self.from_timestamp}&toTimestamp={self.to_timestamp}',
            status=204,
        )

        result = self.dashboard.get_sessions_traces(
            self.from_timestamp, self.to_timestamp
        )
        assert result is None
