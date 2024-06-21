import json
import unittest

from radicalbit_platform_sdk.models import ColumnDefinition


class ColumnDefinitionTest(unittest.TestCase):
    def test_from_json(self):
        field_name = 'age'
        field_type = 'int'
        json_string = f'{{"name": "{field_name}", "type": "{field_type}"}}'
        column_definition = ColumnDefinition.model_validate(json.loads(json_string))
        assert column_definition.name == field_name
        assert column_definition.type == field_type
