import json
import time
import unittest

from radicalbit_platform_sdk.models import ApiKeyDefinition


class ApiKeyDefinitionTest(unittest.TestCase):
    @staticmethod
    def test_api_key_definition_from_json():
        name = 'api_key'
        api_key = 'sk-rb-gdxK0lDmt5ZMqnSUi3xbq82W4O7Bmax8Q1HhYBEO91nnBwKE'
        ts = str(time.time())
        json_string = f"""{{
                "name": "{name}",
                "api_key": "{api_key}",
                "createdAt": "{ts}",
                "updatedAt": "{ts}"
            }}"""
        project_definition = ApiKeyDefinition.model_validate(json.loads(json_string))
        assert project_definition.name == name
        assert project_definition.api_key == api_key
        assert project_definition.created_at == ts
        assert project_definition.updated_at == ts
