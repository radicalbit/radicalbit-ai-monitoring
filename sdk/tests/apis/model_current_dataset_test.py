from radicalbit_platform_sdk.apis import ModelCurrentDataset
from radicalbit_platform_sdk.models import CurrentFileUpload, ModelType, JobStatus, DriftAlgorithm
from radicalbit_platform_sdk.errors import ClientError
import responses
import unittest
import uuid


class ModelCurrentDatasetTest(unittest.TestCase):
    @responses.activate
    def test_statistics_ok(self):
        base_url = "http://api:9000"
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        n_variables = 10
        n_observations = 1000
        missing_cells = 10
        missing_cells_perc = 1
        duplicate_rows = 10
        duplicate_rows_perc = 1
        numeric = 3
        categorical = 6
        datetime = 1
        model_reference_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path="s3://bucket/file.csv",
                date="2014",
                correlation_id_column="column",
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/statistics",
                "status": 200,
                "body": f"""{{
                    "datetime": "something_not_used",
                    "jobStatus": "SUCCEEDED",
                    "statistics": {{
                        "nVariables": {n_variables},
                        "nObservations": {n_observations},
                        "missingCells": {missing_cells},
                        "missingCellsPerc": {missing_cells_perc},
                        "duplicateRows": {duplicate_rows},
                        "duplicateRowsPerc": {duplicate_rows_perc},
                        "numeric": {numeric},
                        "categorical": {categorical},
                        "datetime": {datetime}
                    }}
                }}""",
            }
        )

        stats = model_reference_dataset.statistics()

        assert stats.n_variables == n_variables
        assert stats.n_observations == n_observations
        assert stats.missing_cells == missing_cells
        assert stats.missing_cells_perc == missing_cells_perc
        assert stats.duplicate_rows == duplicate_rows
        assert stats.duplicate_rows_perc == duplicate_rows_perc
        assert stats.numeric == numeric
        assert stats.categorical == categorical
        assert stats.datetime == datetime
        assert model_reference_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_statistics_validation_error(self):
        base_url = "http://api:9000"
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_reference_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path="s3://bucket/file.csv",
                date="2014",
                correlation_id_column="column",
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/statistics",
                "status": 200,
                "body": '{"statistics": "wrong"}',
            }
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.statistics()

    @responses.activate
    def test_statistics_key_error(self):
        base_url = "http://api:9000"
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_reference_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path="s3://bucket/file.csv",
                date="2014",
                correlation_id_column="column",
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/statistics",
                "status": 200,
                "body": '{"wrong": "json"}',
            }
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.statistics()

    @responses.activate
    def test_drift_ok(self):
        base_url = "http://api:9000"
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_reference_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path="s3://bucket/file.csv",
                date="2014",
                correlation_id_column="column",
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/drift",
                "status": 200,
                "body": f"""{{
                    "jobStatus": "SUCCEEDED",
                    "drift": {{
                        "featureMetrics": [
                            {{
                                "featureName": "gender",
                                "driftCalc": {{"type": "CHI2", "value": 0.87, "hasDrift": true}}
                            }},
                            {{
                                "featureName": "city",
                                "driftCalc": {{"type": "CHI2", "value": 0.12, "hasDrift": false}}
                            }},
                            {{
                                "featureName": "age",
                                "driftCalc": {{"type": "KS", "value": 0.92, "hasDrift": true}}
                            }}
                        ]
                    }}
                }}""",
            }
        )

        drift = model_reference_dataset.drift()

        assert len(drift.feature_metrics) == 3
        assert drift.feature_metrics[1].feature_name == "city"
        assert drift.feature_metrics[1].drift_calc.type == DriftAlgorithm.CHI2
        assert drift.feature_metrics[1].drift_calc.value == 0.12
        assert drift.feature_metrics[1].drift_calc.has_drift is False
        assert drift.feature_metrics[2].feature_name == "age"
        assert drift.feature_metrics[2].drift_calc.type == DriftAlgorithm.KS
        assert drift.feature_metrics[2].drift_calc.value == 0.92
        assert drift.feature_metrics[2].drift_calc.has_drift is True
        assert model_reference_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_drift_validation_error(self):
        base_url = "http://api:9000"
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_reference_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path="s3://bucket/file.csv",
                date="2014",
                correlation_id_column="column",
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/drift",
                "status": 200,
                "body": '{"statistics": "wrong"}',
            }
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.drift()

    @responses.activate
    def test_drift_key_error(self):
        base_url = "http://api:9000"
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_reference_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path="s3://bucket/file.csv",
                date="2014",
                correlation_id_column="column",
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            **{
                "method": responses.GET,
                "url": f"{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/drift",
                "status": 200,
                "body": '{"wrong": "json"}',
            }
        )

        with self.assertRaises(ClientError):
            model_reference_dataset.drift()
