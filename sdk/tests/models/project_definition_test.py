import json
import time
import unittest
import uuid

from radicalbit_platform_sdk.models import ProjectDefinition


class ProjectDefinitionTest(unittest.TestCase):
    def test_project_definition_from_json(self):
        id = uuid.uuid4()
        name = 'my project'
        ts = str(time.time())
        json_string = f"""{{
                "uuid": "{str(id)}",
                "name": "{name}",
                "createdAt": "{ts}",
                "updatedAt": "{ts}"
            }}"""
        project_definition = ProjectDefinition.model_validate(json.loads(json_string))
        assert project_definition.uuid == id
        assert project_definition.name == name
        assert project_definition.created_at == ts
        assert project_definition.updated_at == ts
