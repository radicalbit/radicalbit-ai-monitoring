from datetime import datetime
import unittest
import uuid

import responses

from radicalbit_platform_sdk.apis import TracingSession
from radicalbit_platform_sdk.models import Session


class TracingSessionTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://api:9000'
        self.project_uuid = uuid.uuid4()
        self.tracing_session = TracingSession(
            self.base_url,
            self.project_uuid,
            Session(
                project_uuid=self.project_uuid,
                session_uuid=uuid.uuid4(),
                traces=5,
                duration_ms=1200,
                number_of_errors=1,
                created_at=str(datetime.now()),
                latest_trace_ts=str(datetime.now()),
            ),
        )

    @responses.activate
    def test_delete_traces(self):
        responses.add(
            method=responses.DELETE,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/session/{self.tracing_session.uuid()}',
            status=204,
        )
        self.tracing_session.delete_traces()
