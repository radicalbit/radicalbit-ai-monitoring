from datetime import datetime
import unittest
import uuid

import responses

from radicalbit_platform_sdk.apis import TracingRootTrace
from radicalbit_platform_sdk.models import Span, Trace


class TracingRootTraceTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://api:9000'
        self.project_uuid = uuid.uuid4()
        self.tracing_root_trace = TracingRootTrace(
            self.base_url,
            self.project_uuid,
            Trace(
                project_uuid=self.project_uuid,
                trace_id=str(uuid.uuid4()),
                span_id=str(uuid.uuid4()),
                session_uuid=uuid.uuid4(),
                spans=5,
                duration_ms=1200,
                number_of_errors=1,
                created_at=str(datetime.now()),
                latest_span_ts=str(datetime.now()),
            ),
        )

    @responses.activate
    def test_delete_trace(self):
        responses.add(
            method=responses.DELETE,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/{self.tracing_root_trace.id()}',
            status=204,
        )
        self.tracing_root_trace.delete_trace()

    @responses.activate
    def test_get_trace(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/{self.tracing_root_trace.id()}',
            status=200,
            json={
                'projectUuid': str(self.project_uuid),
                'traceId': self.tracing_root_trace.id(),
                'spanId': str(uuid.uuid4()),
                'sessionUuid': str(uuid.uuid4()),
                'spans': 3,
                'durationMs': 500,
                'numberOfErrors': 0,
                'createdAt': str(datetime.now()),
                'latestSpanTs': str(datetime.now()),
            },
        )
        trace = self.tracing_root_trace.get_trace()
        assert isinstance(trace, Trace)
        assert trace.spans == 3
        assert trace.tree is None

    @responses.activate
    def test_get_trace_no_content(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/{self.tracing_root_trace.id()}',
            status=204,
        )
        trace = self.tracing_root_trace.get_trace()
        assert trace is None

    @responses.activate
    def test_get_span(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/{self.tracing_root_trace.id()}/span/{self.tracing_root_trace.span_id()}',
            status=200,
            json={
                'id': self.tracing_root_trace.span_id(),
                'name': 'test_span',
                'traceId': self.tracing_root_trace.id(),
                'projectUuid': str(self.project_uuid),
                'durationsMs': 200,
                'sessionUuid': str(uuid.uuid4()),
                'attributes': {},
                'createdAt': str(datetime.now()),
                'errorEvents': [],
            },
        )
        span = self.tracing_root_trace.get_span()
        assert isinstance(span, Span)
        assert span.trace_id == self.tracing_root_trace.id()

    @responses.activate
    def test_get_span_no_content(self):
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/{self.tracing_root_trace.id()}/span/{self.tracing_root_trace.span_id()}',
            status=204,
        )
        span = self.tracing_root_trace.get_span()
        assert span is None
