from datetime import datetime
import time
import unittest
import uuid

import responses

from radicalbit_platform_sdk.apis import Project, TracingRootTrace, TracingSession
from radicalbit_platform_sdk.models import (
    ApiKeyDefinition,
    CreateApiKey,
    ProjectDefinition,
)


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

    @responses.activate
    def test_create_api_key(self):
        api_key = CreateApiKey(
            name='key',
        )
        api_key_definition = ApiKeyDefinition(
            name=api_key.name,
            api_key='sk-rb-Fndianwdindwa',
            project_uuid=self.project_uuid,
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )
        responses.add(
            method=responses.POST,
            url=f'{self.base_url}/api/api-key/project/{str(self.project_uuid)}',
            body=api_key_definition.model_dump_json(),
            status=201,
            content_type='application/json',
        )

        api_key = self.project.create_api_key(api_key)
        assert api_key.name == api_key_definition.name
        assert api_key.project_uuid == self.project_uuid

    @responses.activate
    def test_get_single_api_key(self):
        name = 'api-key'
        api_key_definition = ApiKeyDefinition(
            name=name,
            api_key='sk-rb-Fndianwdindwa',
            project_uuid=self.project_uuid,
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/api-key/project/{str(self.project_uuid)}/api-keys/{name}',
            body=api_key_definition.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        api_key = self.project.get_api_key(name)
        assert api_key.name == api_key_definition.name
        assert api_key.project_uuid == api_key_definition.project_uuid

    @responses.activate
    def test_search_api_keys(self):
        name_one = 'api-key-onw'
        name_two = 'api-key-two'
        api_key_definition_one = ApiKeyDefinition(
            name=name_one,
            api_key='sk-rb-Fndianwdindwa',
            project_uuid=self.project_uuid,
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )
        api_key_definition_two = ApiKeyDefinition(
            name=name_two,
            api_key='sk-rb-Fnfawfaindwjgj',
            project_uuid=self.project_uuid,
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )
        responses.add(
            method=responses.GET,
            url=f'{self.base_url}/api/api-key/project/{str(self.project_uuid)}/all',
            body=f'[{api_key_definition_one.model_dump_json()}, {api_key_definition_two.model_dump_json()}]',
            status=200,
            content_type='application/json',
        )

        api_keys = self.project.search_api_keys()
        assert len(api_keys) == 2
        assert api_keys[0].name == api_key_definition_one.name
        assert api_keys[0].project_uuid == api_key_definition_one.project_uuid
        assert api_keys[1].name == api_key_definition_two.name
        assert api_keys[1].project_uuid == api_key_definition_two.project_uuid

    @responses.activate
    def test_delete_api(self):
        name = 'api-key'
        responses.add(
            method=responses.DELETE,
            url=f'{self.base_url}/api/api-key/project/{self.project_uuid}/api-keys/{name}',
            status=204,
        )
        self.project.delete_api_key(name)
