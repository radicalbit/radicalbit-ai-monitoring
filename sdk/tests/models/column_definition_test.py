import json
import unittest

from radicalbit_platform_sdk.models import ColumnDefinition, FieldType, SupportedTypes


class ColumnDefinitionTest(unittest.TestCase):
    def test_from_json(self):
        name = 'age'
        type = 'int'
        field_type = 'numerical'
        json_string = (
            f'{{"name": "{name}", "type": "{type}", "fieldType": "{field_type}"}}'
        )
        column_definition = ColumnDefinition.model_validate(json.loads(json_string))
        assert column_definition.name == name
        assert column_definition.type == SupportedTypes.int
        assert column_definition.field_type == FieldType.numerical
