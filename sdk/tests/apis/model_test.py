import time
import unittest
import uuid

import boto3
from moto import mock_aws
import pytest
import responses

from radicalbit_platform_sdk.apis import Model
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    ColumnDefinition,
    CurrentFileUpload,
    DataType,
    Granularity,
    JobStatus,
    ModelDefinition,
    ModelType,
    OutputType,
    ReferenceFileUpload,
)


class ModelTest(unittest.TestCase):
    @responses.activate
    def test_delete_model(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        column_def = ColumnDefinition(name='column', type='my_type')
        outputs = OutputType(prediction=column_def, output=[column_def])
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.MONTH,
                features=[],
                outputs=outputs,
                target=column_def,
                timestamp=column_def,
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        responses.add(
            method=responses.DELETE,
            url=f'{base_url}/api/models/{str(model_id)}',
            status=200,
        )
        model.delete()

    @mock_aws
    @responses.activate
    def test_load_reference_dataset_without_object_name(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        bucket_name = 'test-bucket'
        file_name = 'test.txt'
        column_def = ColumnDefinition(name='prediction', type='float')
        expected_path = f's3://{bucket_name}/{model_id}/reference/{file_name}'
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket_name)
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.HOUR,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        response = ReferenceFileUpload(
            uuid=uuid.uuid4(), path=expected_path, date='', status=JobStatus.IMPORTING
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models/{str(model_id)}/reference/bind',
            body=response.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        response = model.load_reference_dataset(
            'tests_resources/people.csv', bucket_name
        )
        assert response.path() == expected_path

    @mock_aws
    @responses.activate
    def test_load_reference_dataset_with_different_separator(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        bucket_name = 'test-bucket'
        file_name = 'test.txt'
        column_def = ColumnDefinition(name='prediction', type='float')
        expected_path = f's3://{bucket_name}/{model_id}/reference/{file_name}'
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket_name)
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.DAY,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        response = ReferenceFileUpload(
            uuid=uuid.uuid4(), path=expected_path, date='', status=JobStatus.IMPORTING
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models/{str(model_id)}/reference/bind',
            body=response.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        response = model.load_reference_dataset(
            'tests_resources/people_pipe_separated.csv', bucket_name, separator='|'
        )
        assert response.path() == expected_path

    @mock_aws
    @responses.activate
    def test_load_reference_dataset_with_object_name(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        bucket_name = 'test-bucket'
        file_name = 'test.txt'
        column_def = ColumnDefinition(name='prediction', type='float')
        expected_path = f's3://{bucket_name}/{file_name}'
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket_name)
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.WEEK,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        response = ReferenceFileUpload(
            uuid=uuid.uuid4(), path=expected_path, date='', status=JobStatus.IMPORTING
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models/{str(model_id)}/reference/bind',
            body=response.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        response = model.load_reference_dataset(
            'tests_resources/people.csv', bucket_name
        )
        assert response.path() == expected_path

    def test_load_reference_dataset_wrong_headers(self):
        column_def = ColumnDefinition(name='prediction', type='float')
        model = Model(
            'http://api:9000',
            ModelDefinition(
                uuid=uuid.uuid4(),
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.MONTH,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        with pytest.raises(ClientError):
            model.load_reference_dataset('tests_resources/wrong.csv', 'bucket_name')

    @mock_aws
    @responses.activate
    def test_load_current_dataset_without_object_name(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        bucket_name = 'test-bucket'
        file_name = 'test.txt'
        column_def = ColumnDefinition(name='prediction', type='float')
        expected_path = f's3://{bucket_name}/{model_id}/reference/{file_name}'
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket_name)
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.DAY,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        response = CurrentFileUpload(
            uuid=uuid.uuid4(),
            path=expected_path,
            date='',
            status=JobStatus.IMPORTING,
            correlation_id_column='correlation',
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models/{str(model_id)}/current/bind',
            body=response.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        response = model.load_current_dataset(
            'tests_resources/people_current.csv',
            bucket_name,
            response.correlation_id_column,
        )
        assert response.path() == expected_path

    @mock_aws
    @responses.activate
    def test_load_current_dataset_with_object_name(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        bucket_name = 'test-bucket'
        file_name = 'test.txt'
        column_def = ColumnDefinition(name='prediction', type='float')
        expected_path = f's3://{bucket_name}/{file_name}'
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket=bucket_name)
        model = Model(
            base_url,
            ModelDefinition(
                uuid=model_id,
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.HOUR,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        response = CurrentFileUpload(
            uuid=uuid.uuid4(),
            path=expected_path,
            date='',
            status=JobStatus.IMPORTING,
            correlation_id_column='correlation',
        )
        responses.add(
            method=responses.POST,
            url=f'{base_url}/api/models/{str(model_id)}/current/bind',
            body=response.model_dump_json(),
            status=200,
            content_type='application/json',
        )
        response = model.load_current_dataset(
            'tests_resources/people_current.csv',
            bucket_name,
            response.correlation_id_column,
        )
        assert response.path() == expected_path

    def test_load_current_dataset_wrong_headers(self):
        column_def = ColumnDefinition(name='prediction', type='float')
        model = Model(
            'http://api:9000',
            ModelDefinition(
                uuid=uuid.uuid4(),
                name='My Model',
                model_type=ModelType.BINARY,
                data_type=DataType.TABULAR,
                granularity=Granularity.MONTH,
                features=[
                    ColumnDefinition(name='first_name', type='str'),
                    ColumnDefinition(name='age', type='int'),
                ],
                outputs=OutputType(prediction=column_def, output=[column_def]),
                target=ColumnDefinition(name='adult', type='bool'),
                timestamp=ColumnDefinition(name='created_at', type='str'),
                created_at=str(time.time()),
                updated_at=str(time.time()),
            ),
        )
        with pytest.raises(ClientError):
            model.load_current_dataset(
                'tests_resources/wrong.csv', 'bucket_name', 'correlation'
            )
