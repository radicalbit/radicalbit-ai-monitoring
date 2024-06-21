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
    Granularity,
    ModelDefinition,
    ModelType,
    OutputType,
    PaginatedModelDefinitions,
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
        output_name = 'adult'
        output_type = 'bool'
        target_name = 'adult'
        target_type = 'bool'
        timestamp_name = 'when'
        timestamp_type = 'str'
        ts = str(time.time())
        json_string = f"""{{
                "uuid": "{str(model_id)}",
                "name": "{name}",
                "modelType": "{model_type.value}",
                "dataType": "{data_type.value}",
                "granularity": "{granularity.value}",
                "features": [{{
                    "name": "{feature_name}",
                    "type": "{feature_type}"
                }}],
                "outputs": {{
                    "prediction": {{
                        "name": "{output_name}",
                        "type": "{output_type}"
                    }},
                    "predictionProba": {{
                        "name": "{output_name}",
                        "type": "{output_type}"
                    }},
                    "output": [{{
                        "name": "{output_name}",
                        "type": "{output_type}"
                    }}]
                }},
                "target": {{
                    "name": "{target_name}",
                    "type": "{target_type}"
                }},
                "timestamp": {{
                    "name": "{timestamp_name}",
                    "type": "{timestamp_type}"
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
        assert model.target().type == target_type
        assert model.timestamp().name == timestamp_name
        assert model.timestamp().type == timestamp_type
        assert len(model.features()) == 1
        assert model.features()[0].name == feature_name
        assert model.features()[0].type == feature_type
        assert model.outputs().prediction.name == output_name
        assert model.outputs().prediction.type == output_type
        assert model.outputs().prediction_proba.name == output_name
        assert model.outputs().prediction_proba.type == output_type
        assert len(model.outputs().output) == 1
        assert model.outputs().output[0].name == output_name
        assert model.outputs().output[0].type == output_type

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
            features=[ColumnDefinition(name='feature_column', type='string')],
            outputs=OutputType(
                prediction=ColumnDefinition(name='result_column', type='int'),
                output=[ColumnDefinition(name='result_column', type='int')],
            ),
            target=ColumnDefinition(name='target_column', type='string'),
            timestamp=ColumnDefinition(name='tst_column', type='string'),
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
    def test_search_models(self):
        base_url = 'http://api:9000'

        paginated_response = PaginatedModelDefinitions(
            items=[
                ModelDefinition(
                    name='My Model',
                    model_type=ModelType.BINARY,
                    data_type=DataType.TABULAR,
                    granularity=Granularity.DAY,
                    features=[ColumnDefinition(name='feature_column', type='string')],
                    outputs=OutputType(
                        prediction=ColumnDefinition(name='result_column', type='int'),
                        output=[ColumnDefinition(name='result_column', type='int')],
                    ),
                    target=ColumnDefinition(name='target_column', type='string'),
                    timestamp=ColumnDefinition(name='tst_column', type='string'),
                    created_at=str(time.time()),
                    updated_at=str(time.time()),
                )
            ]
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models',
            body=paginated_response.model_dump_json(),
            status=200,
            content_type='application/json',
        )

        client = Client(base_url)
        models = client.search_models()
        assert len(models) == 1
        assert models[0].name() == paginated_response.items[0].name
        assert models[0].model_type() == paginated_response.items[0].model_type
        assert models[0].data_type() == paginated_response.items[0].data_type
        assert models[0].granularity() == paginated_response.items[0].granularity
        assert models[0].features() == paginated_response.items[0].features
        assert models[0].outputs() == paginated_response.items[0].outputs
        assert models[0].target() == paginated_response.items[0].target
        assert models[0].timestamp() == paginated_response.items[0].timestamp
        assert models[0].description() is None
        assert models[0].algorithm() is None
        assert models[0].frameworks() is None
