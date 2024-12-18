import unittest
import uuid

import pytest
import responses

from radicalbit_platform_sdk.apis import ModelCompletionDataset
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    CompletionFileUpload,
    CompletionTextGenerationModelQuality,
    JobStatus,
    ModelType,
)


class ModelCompletionDatasetTest(unittest.TestCase):
    @responses.activate
    def test_text_generation_model_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_completion_dataset = ModelCompletionDataset(
            base_url,
            model_id,
            ModelType.TEXT_GENERATION,
            CompletionFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.json',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/completion/{str(import_uuid)}/model-quality',
            status=200,
            body="""{
                    "datetime": "something_not_used",
                    "jobStatus": "SUCCEEDED",
                    "modelQuality": {}
                }""",
        )

        metrics = model_completion_dataset.model_quality()

        assert isinstance(metrics, CompletionTextGenerationModelQuality)
        assert model_completion_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_model_quality_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_completion_dataset = ModelCompletionDataset(
            base_url,
            model_id,
            ModelType.TEXT_GENERATION,
            CompletionFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.json',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/completion/{str(import_uuid)}/model-quality',
            status=200,
            body='{"modelQuality": "wrong"}',
        )

        with pytest.raises(ClientError):
            model_completion_dataset.model_quality()

    @responses.activate
    def test_model_quality_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_completion_dataset = ModelCompletionDataset(
            base_url,
            model_id,
            ModelType.TEXT_GENERATION,
            CompletionFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.json',
                date='2014',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/completion/{str(import_uuid)}/model-quality',
            status=200,
            body='{"wrong": "json"}',
        )

        with pytest.raises(ClientError):
            model_completion_dataset.model_quality()
