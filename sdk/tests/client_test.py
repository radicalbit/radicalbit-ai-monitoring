import time
import unittest
import uuid

import pytest
import responses

from radicalbit_platform_sdk.client import Client
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    ColumnDefinition,
    CreateModel,
    DataType,
    FieldType,
    Granularity,
    ModelDefinition,
    ModelType,
    OutputType,
    SupportedTypes,
)


class ClientTest(unittest.TestCase):
    @responses.activate
    def test_get_model(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        name = 'My super Model'
        model_type = ModelType.MULTI_CLASS
        data_type = DataType.IMAGE
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
                "uuid": "{str(model_id)}",
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
        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}',
            body=json_string,
            status=200,
            content_type='application/json',
        )
        client = Client(base_url)
        model = client.get_model(id=model_id)

        assert model.name() == name
        assert model.model_type() == model_type
        assert model.data_type() == data_type
        assert model.granularity() == granularity
        assert model.description() == description
        assert model.algorithm() == algorithm
        assert model.frameworks() == frameworks
        assert model.target().name == target_name
        assert model.target().type == SupportedTypes.bool
        assert model.target().field_type == FieldType.categorical
        assert model.timestamp().name == timestamp_name
        assert model.timestamp().type == SupportedTypes.datetime
        assert model.timestamp().field_type == FieldType.datetime
        assert len(model.features()) == 1
        assert model.features()[0].name == feature_name
        assert model.features()[0].type == SupportedTypes.int
        assert model.features()[0].field_type == FieldType.numerical
        assert model.outputs().prediction.name == output_name
        assert model.outputs().prediction.type == SupportedTypes.bool
        assert model.outputs().prediction.field_type == FieldType.categorical
        assert model.outputs().prediction_proba.name == output_name
        assert model.outputs().prediction_proba.type == SupportedTypes.bool
        assert model.outputs().prediction_proba.field_type == FieldType.categorical
        assert len(model.outputs().output) == 1
        assert model.outputs().output[0].name == output_name
        assert model.outputs().output[0].type == SupportedTypes.bool
        assert model.outputs().output[0].field_type == FieldType.categorical

    @responses.activate
    def test_get_model_client_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        invalid_json = '{"name": "Random Name"}'
        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}',
            body=invalid_json,
            status=200,
            content_type='application/json',
        )
        client = Client(base_url)
        with pytest.raises(ClientError):
            client.get_model(id=model_id)

    @responses.activate
    def test_create_model(self):
        base_url = 'http://api:9000'
        model = CreateModel(
            name='My Model',
            model_type=ModelType.BINARY,
            data_type=DataType.TABULAR,
            granularity=Granularity.WEEK,
            features=[
                ColumnDefinition(
                    name='feature_column',
                    type=SupportedTypes.string,
                    field_type=FieldType.categorical,
                )
            ],
            outputs=OutputType(
                prediction=ColumnDefinition(
                    name='result_column',
                    type=SupportedTypes.int,
                    field_type=FieldType.numerical,
                ),
                output=[
                    ColumnDefinition(
                        name='result_column',
                        type=SupportedTypes.int,
                        field_type=FieldType.numerical,
                    )
                ],
            ),
            target=ColumnDefinition(
                name='target_column',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            ),
            timestamp=ColumnDefinition(
                name='tst_column',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            ),
        )
        model_definition = ModelDefinition(
            name=model.name,
            model_type=model.model_type,
            data_type=model.data_type,
            granularity=model.granularity,
            features=model.features,
            outputs=model.outputs,
            target=model.target,
            timestamp=model.timestamp,
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models',
            body=model_definition.model_dump_json(),
            status=201,
            content_type='application/json',
        )

        client = Client(base_url)
        model = client.create_model(model)
        assert model.name() == model_definition.name
        assert model.model_type() == model_definition.model_type
        assert model.data_type() == model_definition.data_type
        assert model.granularity() == model_definition.granularity
        assert model.features() == model_definition.features
        assert model.outputs() == model_definition.outputs
        assert model.target() == model_definition.target
        assert model.timestamp() == model_definition.timestamp
        assert model.description() is None
        assert model.algorithm() is None
        assert model.frameworks() is None

    @responses.activate
    def test_create_model_with_empty_schema(self):
        base_url = 'http://api:9000'
        model = CreateModel(
            name='My Model',
            model_type=ModelType.TEXT_GENERATION,
            data_type=DataType.TEXT,
            granularity=Granularity.DAY,
            features=None,
            outputs=None,
            target=None,
            timestamp=None
        )

        model_definition = ModelDefinition(
            name=model.name,
            model_type=model.model_type,
            data_type=model.data_type,
            granularity=model.granularity,
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models',
            body=model_definition.model_dump_json(),
            status=201,
            content_type='application/json',
        )

        client = Client(base_url)
        model = client.create_model(model)
        assert model.name() == model_definition.name
        assert model.model_type() == model_definition.model_type
        assert model.data_type() == model_definition.data_type
        assert model.granularity() == model_definition.granularity
        assert model.features() is None
        assert model.outputs() is None
        assert model.target() is None
        assert model.timestamp() is None
        assert model.description() is None
        assert model.algorithm() is None
        assert model.frameworks() is None

    @responses.activate
    def test_search_models(self):
        base_url = 'http://api:9000'

        model_definition = ModelDefinition(
            name='My Model',
            model_type=ModelType.BINARY,
            data_type=DataType.TABULAR,
            granularity=Granularity.DAY,
            features=[
                ColumnDefinition(
                    name='feature_column',
                    type=SupportedTypes.string,
                    field_type=FieldType.categorical,
                )
            ],
            outputs=OutputType(
                prediction=ColumnDefinition(
                    name='result_column',
                    type=SupportedTypes.int,
                    field_type=FieldType.numerical,
                ),
                output=[
                    ColumnDefinition(
                        name='result_column',
                        type=SupportedTypes.int,
                        field_type=FieldType.numerical,
                    )
                ],
            ),
            target=ColumnDefinition(
                name='target_column',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            ),
            timestamp=ColumnDefinition(
                name='tst_column',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            ),
            created_at=str(time.time()),
            updated_at=str(time.time()),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/all',
            body=f'[{model_definition.model_dump_json()}]',
            status=200,
            content_type='application/json',
        )

        client = Client(base_url)
        models = client.search_models()
        assert len(models) == 1
        assert models[0].name() == model_definition.name
        assert models[0].model_type() == model_definition.model_type
        assert models[0].data_type() == model_definition.data_type
        assert models[0].granularity() == model_definition.granularity
        assert models[0].features() == model_definition.features
        assert models[0].outputs() == model_definition.outputs
        assert models[0].target() == model_definition.target
        assert models[0].timestamp() == model_definition.timestamp
        assert models[0].description() is None
        assert models[0].algorithm() is None
        assert models[0].frameworks() is None
