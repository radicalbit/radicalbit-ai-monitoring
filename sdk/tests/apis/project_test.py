import time
import unittest
import uuid

import responses

from radicalbit_platform_sdk.apis import Project
from radicalbit_platform_sdk.models import ProjectDefinition


class ProjectTest(unittest.TestCase):
    @responses.activate
    def test_delete_project(self):
        base_url = 'http://api:9000'
        project_id = uuid.uuid4()
        project = Project(
            base_url,
            ProjectDefinition(
                uuid=project_id,
                name='my project',
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        responses.add(
            method=responses.DELETE,
            url=f'{base_url}/api/projects/{str(project_id)}',
            status=200,
        )
        project.delete()
