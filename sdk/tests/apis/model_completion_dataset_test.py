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
                    "modelQuality":
                        {
                            "tokens": [
                                {
                                    "id": "chatcmpl",
                                    "message_content": "Sky is blue.",
                                    "probs":[
                                        {
                                            "prob":0.27,
                                            "token":"Sky"
                                        },
                                        {
                                            "prob":0.89,
                                            "token":" is"
                                        },
                                        {
                                            "prob":0.70,
                                            "token":" blue"
                                        },
                                        {
                                            "prob":0.99,
                                            "token":"."
                                        }
                                    ]
                                }
                            ],
                            "mean_per_file":[
                                {
                                    "prob_tot_mean":0.71,
                                    "perplex_tot_mean":1.52
                                }
                            ],
                            "mean_per_phrase":[
                                {
                                    "id":"chatcmpl",
                                    "prob_per_phrase":0.71,
                                    "perplex_per_phrase":1.54
                                }
                            ]
                        }
                    }""",
        )

        metrics = model_completion_dataset.model_quality()

        assert isinstance(metrics, CompletionTextGenerationModelQuality)
        assert metrics.tokens[0].message_content == 'Sky is blue.'
        assert metrics.tokens[0].probs[0].prob == 0.27
        assert metrics.tokens[0].probs[0].token == 'Sky'
        assert metrics.mean_per_file[0].prob_tot_mean == 0.71
        assert metrics.mean_per_file[0].perplex_tot_mean == 1.52
        assert metrics.mean_per_phrase[0].prob_per_phrase == 0.71
        assert metrics.mean_per_phrase[0].perplex_per_phrase == 1.54
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
