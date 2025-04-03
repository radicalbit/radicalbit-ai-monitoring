from datetime import datetime
import time
import unittest
import uuid

import responses

from radicalbit_platform_sdk.apis import Project, TracingRootTrace, TracingSession
from radicalbit_platform_sdk.models import ProjectDefinition


class ProjectTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://api:9000'
        self.project_uuid = uuid.uuid4()
        self.project = Project(
            self.base_url,
            ProjectDefinition(
                uuid=self.project_uuid,
                name='my project',
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )

    @responses.activate
    def test_delete_project(self):
        responses.add(
            method=responses.DELETE,
            url=f'{self.base_url}/api/projects/{self.project_uuid}',
            status=200,
        )
        self.project.delete()

    @responses.activate
    def test_get_all_sessions(self):
        session_uuid = uuid.uuid4()
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/session/all',
            status=200,
            json=[
                {
                    'projectUuid': str(self.project_uuid),
                    'sessionUuid': str(session_uuid),
                    'traces': 5,
                    'durationMs': 1200,
                    'numberOfErrors': 1,
                    'createdAt': str(datetime.now()),
                    'latestTraceTs': str(datetime.now()),
                }
            ],
        )

        sessions = self.project.get_all_sessions()
        assert isinstance(sessions, list)
        assert isinstance(sessions[0], TracingSession)
        assert sessions[0].uuid() == session_uuid
        assert sessions[0].prompt_tokens() == 0

    @responses.activate
    def test_get_all_root_traces(self):
        trace_id = str(uuid.uuid4())
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/all',
            status=200,
            json=[
                {
                    'projectUuid': str(self.project_uuid),
                    'traceId': trace_id,
                    'spanId': str(uuid.uuid4()),
                    'sessionUuid': str(uuid.uuid4()),
                    'spans': 3,
                    'durationMs': 500,
                    'numberOfErrors': 0,
                    'createdAt': str(datetime.now()),
                    'latestSpanTs': str(datetime.now()),
                }
            ],
        )
        traces = self.project.get_all_root_traces()
        assert len(traces) == 1
        assert isinstance(traces[0], TracingRootTrace)
        assert traces[0].id() == trace_id
        assert traces[0].tree_node() is None

    @responses.activate
    def test_get_all_root_traces_with_params(self):
        trace_id = str(uuid.uuid4())
        session_uuid = uuid.uuid4()
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/traces/project/{self.project_uuid}/trace/all?traceId={trace_id}&sessionUuid={session_uuid}',
            status=200,
            json=[
                {
                    'projectUuid': str(self.project_uuid),
                    'traceId': trace_id,
                    'spanId': str(uuid.uuid4()),
                    'sessionUuid': str(session_uuid),
                    'spans': 3,
                    'durationMs': 500,
                    'numberOfErrors': 0,
                    'createdAt': str(datetime.now()),
                    'latestSpanTs': str(datetime.now()),
                }
            ],
        )
        traces = self.project.get_all_root_traces(trace_id, session_uuid)
        assert len(traces) == 1
        assert isinstance(traces[0], TracingRootTrace)
        assert traces[0].id() == trace_id
        assert traces[0].session_uuid() == session_uuid
