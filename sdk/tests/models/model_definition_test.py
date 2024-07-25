import json
import time
import unittest
import uuid

from radicalbit_platform_sdk.models import (
    DataType,
    FieldType,
    Granularity,
    ModelDefinition,
    ModelType,
    SupportedTypes,
)


class ModelDefinitionTest(unittest.TestCase):
    def test_model_definition_from_json(self):
        id = uuid.uuid4()
        name = 'My super Model'
        model_type = ModelType.BINARY
        data_type = DataType.TEXT
        granularity = Granularity.HOUR
        description = 'some boring description about this model'
        algorithm = 'brainfucker'
        frameworks = 'mlflow'
        feature_name = 'age'
        feature_type = 'int'
        feature_field_type = 'numerical'
        output_name = 'adult'
        output_type = 'bool'
        output_field_type = 'categorical'
        target_name = 'adult'
        target_type = 'bool'
        target_field_type = 'categorical'
        timestamp_name = 'when'
        timestamp_type = 'datetime'
        timestamp_field_type = 'datetime'
        ts = str(time.time())
        json_string = f"""{{
                "uuid": "{str(id)}",
                "name": "{name}",
                "modelType": "{model_type.value}",
                "dataType": "{data_type.value}",
                "granularity": "{granularity.value}",
                "features": [{{
                    "name": "{feature_name}",
                    "type": "{feature_type}",
                    "fieldType": "{feature_field_type}"
                }}],
                "outputs": {{
                    "prediction": {{
                        "name": "{output_name}",
                        "type": "{output_type}",
                        "fieldType": "{output_field_type}"
                    }},
                    "predictionProba": {{
                        "name": "{output_name}",
                        "type": "{output_type}",
                        "fieldType": "{output_field_type}"
                    }},
                    "output": [{{
                        "name": "{output_name}",
                        "type": "{output_type}",
                        "fieldType": "{output_field_type}"
                    }}]
                }},
                "target": {{
                    "name": "{target_name}",
                    "type": "{target_type}",
                    "fieldType": "{target_field_type}"
                }},
                "timestamp": {{
                    "name": "{timestamp_name}",
                    "type": "{timestamp_type}",
                    "fieldType": "{timestamp_field_type}"
                }},
                "description": "{description}",
                "algorithm": "{algorithm}",
                "frameworks": "{frameworks}",
                "createdAt": "{ts}",
                "updatedAt": "{ts}"
            }}"""
        model_definition = ModelDefinition.model_validate(json.loads(json_string))
        assert model_definition.uuid == id
        assert model_definition.name == name
        assert model_definition.model_type == model_type
        assert model_definition.data_type == data_type
        assert model_definition.granularity == granularity
        assert model_definition.description == description
        assert model_definition.algorithm == algorithm
        assert model_definition.frameworks == frameworks
        assert model_definition.created_at == ts
        assert model_definition.updated_at == ts
        assert len(model_definition.features) == 1
        assert model_definition.features[0].name == feature_name
        assert model_definition.features[0].type == SupportedTypes.int
        assert model_definition.features[0].field_type == FieldType.numerical
        assert model_definition.outputs.prediction.name == output_name
        assert model_definition.outputs.prediction.type == SupportedTypes.bool
        assert model_definition.outputs.prediction.field_type == FieldType.categorical
        assert model_definition.outputs.prediction_proba.name == output_name
        assert model_definition.outputs.prediction_proba.type == SupportedTypes.bool
        assert (
            model_definition.outputs.prediction_proba.field_type
            == FieldType.categorical
        )
        assert len(model_definition.outputs.output) == 1
        assert model_definition.outputs.output[0].name == output_name
        assert model_definition.outputs.output[0].type == SupportedTypes.bool
        assert model_definition.outputs.output[0].field_type == FieldType.categorical
        assert model_definition.target.name == target_name
        assert model_definition.target.type == SupportedTypes.bool
        assert model_definition.target.field_type == FieldType.categorical
        assert model_definition.timestamp.name == timestamp_name
        assert model_definition.timestamp.type == SupportedTypes.datetime
        assert model_definition.timestamp.field_type == FieldType.datetime
