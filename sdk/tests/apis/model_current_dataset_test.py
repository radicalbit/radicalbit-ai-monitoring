import unittest
import uuid

import pytest
import responses

from radicalbit_platform_sdk.apis import ModelCurrentDataset
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    ClassificationDataQuality,
    CurrentBinaryClassificationModelQuality,
    CurrentFileUpload,
    CurrentRegressionModelQuality,
    Drift,
    DriftAlgorithm,
    JobStatus,
    ModelType,
    MultiClassificationModelQuality,
    RegressionDataQuality,
)


class ModelCurrentDatasetTest(unittest.TestCase):
    @responses.activate
    def test_statistics_ok(self):
        base_url = 'http://api:9000'
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
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/statistics',
            status=200,
            body=f"""{{
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
        )

        stats = model_current_dataset.statistics()

        assert stats.n_variables == n_variables
        assert stats.n_observations == n_observations
        assert stats.missing_cells == missing_cells
        assert stats.missing_cells_perc == missing_cells_perc
        assert stats.duplicate_rows == duplicate_rows
        assert stats.duplicate_rows_perc == duplicate_rows_perc
        assert stats.numeric == numeric
        assert stats.categorical == categorical
        assert stats.datetime == datetime
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_statistics_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/statistics',
            status=200,
            body='{"statistics": "wrong"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.statistics()

    @responses.activate
    def test_statistics_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/statistics',
            status=200,
            body='{"wrong": "json"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.statistics()

    @responses.activate
    def test_drift_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/drift',
            status=200,
            body="""{
                    "jobStatus": "SUCCEEDED",
                    "drift": {
                        "featureMetrics": [
                            {
                                "featureName": "gender",
                                "driftCalc": {"type": "CHI2", "value": 0.87, "hasDrift": true}
                            },
                            {
                                "featureName": "city",
                                "driftCalc": {"type": "CHI2", "value": 0.12, "hasDrift": false}
                            },
                            {
                                "featureName": "age",
                                "driftCalc": {"type": "KS", "value": 0.92, "hasDrift": true}
                            }
                        ]
                    }
                }""",
        )

        drift = model_current_dataset.drift()

        assert isinstance(drift, Drift)

        assert len(drift.feature_metrics) == 3
        assert drift.feature_metrics[1].feature_name == 'city'
        assert drift.feature_metrics[1].drift_calc.type == DriftAlgorithm.CHI2
        assert drift.feature_metrics[1].drift_calc.value == 0.12
        assert drift.feature_metrics[1].drift_calc.has_drift is False
        assert drift.feature_metrics[2].feature_name == 'age'
        assert drift.feature_metrics[2].drift_calc.type == DriftAlgorithm.KS
        assert drift.feature_metrics[2].drift_calc.value == 0.92
        assert drift.feature_metrics[2].drift_calc.has_drift is True
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_drift_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/drift',
            status=200,
            body='{"statistics": "wrong"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.drift()

    @responses.activate
    def test_drift_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/drift',
            status=200,
            body='{"wrong": "json"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.drift()

    @responses.activate
    def test_binary_class_data_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/data-quality',
            status=200,
            body="""{
                    "datetime": "something_not_used",
                    "jobStatus": "SUCCEEDED",
                    "dataQuality": {
                        "nObservations": 200,
                        "classMetrics": [
                            {"name": "classA", "count": 100, "percentage": 50.0},
                            {"name": "classB", "count": 100, "percentage": 50.0}
                        ],
                        "classMetricsPrediction": [
                            {"name": "classA", "count": 100, "percentage": 50.0},
                            {"name": "classB", "count": 100, "percentage": 50.0}
                        ],
                        "featureMetrics": [
                            {
                                "featureName": "age",
                                "type": "numerical",
                                "mean": 29.5,
                                "std": 5.2,
                                "min": 18,
                                "max": 45,
                                "medianMetrics": {"perc25": 25.0, "median": 29.0, "perc75": 34.0},
                                "missingValue": {"count": 2, "percentage": 0.02},
                                "classMedianMetrics": [
                                    {
                                        "name": "classA",
                                        "mean": 30.0,
                                        "medianMetrics": {"perc25": 27.0, "median": 30.0, "perc75": 33.0}
                                    },
                                    {
                                        "name": "classB",
                                        "mean": 29.0,
                                        "medianMetrics": {"perc25": 24.0, "median": 28.0, "perc75": 32.0}
                                    }
                                ],
                                "histogram": {
                                    "buckets": [40.0, 45.0, 50.0, 55.0, 60.0],
                                    "referenceValues": [50, 150, 200, 150, 50],
                                    "currentValues": [45, 140, 210, 145, 60]
                                }
                            },
                            {
                                "featureName": "gender",
                                "type": "categorical",
                                "distinctValue": 2,
                                "categoryFrequency": [
                                    {"name": "male", "count": 90, "frequency": 0.45},
                                    {"name": "female", "count": 110, "frequency": 0.55}
                                ],
                                "missingValue": {"count": 0, "percentage": 0.0}
                            }
                        ]
                    }
                }""",
        )

        metrics = model_current_dataset.data_quality()

        assert isinstance(metrics, ClassificationDataQuality)

        assert metrics.n_observations == 200
        assert len(metrics.class_metrics) == 2
        assert metrics.class_metrics[0].name == 'classA'
        assert metrics.class_metrics[0].count == 100
        assert metrics.class_metrics[0].percentage == 50.0
        assert metrics.class_metrics_prediction[0].name == 'classA'
        assert metrics.class_metrics_prediction[0].count == 100
        assert metrics.class_metrics_prediction[0].percentage == 50.0
        assert len(metrics.feature_metrics) == 2
        assert metrics.feature_metrics[0].feature_name == 'age'
        assert metrics.feature_metrics[0].type == 'numerical'
        assert metrics.feature_metrics[0].mean == 29.5
        assert metrics.feature_metrics[1].feature_name == 'gender'
        assert metrics.feature_metrics[1].type == 'categorical'
        assert metrics.feature_metrics[1].distinct_value == 2
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_multi_class_data_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.MULTI_CLASS,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/data-quality',
            status=200,
            body="""{
                                "datetime": "something_not_used",
                                "jobStatus": "SUCCEEDED",
                                "dataQuality": {
                                    "nObservations": 200,
                                    "classMetrics": [
                                        {"name": "classA", "count": 100, "percentage": 50.0},
                                        {"name": "classB", "count": 100, "percentage": 50.0}
                                    ],
                                   "classMetricsPrediction": [
                                        {"name": "classA", "count": 100, "percentage": 50.0},
                                        {"name": "classB", "count": 100, "percentage": 50.0}
                                    ],
                                    "featureMetrics": [
                                        {
                                            "featureName": "age",
                                            "type": "numerical",
                                            "mean": 29.5,
                                            "std": 5.2,
                                            "min": 18,
                                            "max": 45,
                                            "medianMetrics": {"perc25": 25.0, "median": 29.0, "perc75": 34.0},
                                            "missingValue": {"count": 2, "percentage": 0.02},
                                            "classMedianMetrics": [
                                                {
                                                    "name": "classA",
                                                    "mean": 30.0,
                                                    "medianMetrics": {"perc25": 27.0, "median": 30.0, "perc75": 33.0}
                                                },
                                                {
                                                    "name": "classB",
                                                    "mean": 29.0,
                                                    "medianMetrics": {"perc25": 24.0, "median": 28.0, "perc75": 32.0}
                                                }
                                            ],
                                            "histogram": {
                                                "buckets": [40.0, 45.0, 50.0, 55.0, 60.0],
                                                "referenceValues": [50, 150, 200, 150, 50],
                                                "currentValues": [45, 140, 210, 145, 60]
                                            }
                                        },
                                        {
                                            "featureName": "gender",
                                            "type": "categorical",
                                            "distinctValue": 2,
                                            "categoryFrequency": [
                                                {"name": "male", "count": 90, "frequency": 0.45},
                                                {"name": "female", "count": 110, "frequency": 0.55}
                                            ],
                                            "missingValue": {"count": 0, "percentage": 0.0}
                                        }
                                    ]
                                }
                            }""",
        )

        metrics = model_current_dataset.data_quality()

        assert isinstance(metrics, ClassificationDataQuality)

        assert metrics.n_observations == 200
        assert len(metrics.class_metrics) == 2
        assert metrics.class_metrics[0].name == 'classA'
        assert metrics.class_metrics[0].count == 100
        assert metrics.class_metrics[0].percentage == 50.0
        assert metrics.class_metrics_prediction[0].name == 'classA'
        assert metrics.class_metrics_prediction[0].count == 100
        assert metrics.class_metrics_prediction[0].percentage == 50.0
        assert len(metrics.feature_metrics) == 2
        assert metrics.feature_metrics[0].feature_name == 'age'
        assert metrics.feature_metrics[0].type == 'numerical'
        assert metrics.feature_metrics[0].mean == 29.5
        assert metrics.feature_metrics[1].feature_name == 'gender'
        assert metrics.feature_metrics[1].type == 'categorical'
        assert metrics.feature_metrics[1].distinct_value == 2
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_regression_data_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.REGRESSION,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/data-quality',
            status=200,
            body="""{
                    "datetime": "something_not_used",
                    "jobStatus": "SUCCEEDED",
                    "dataQuality": {
                        "n_observations":731,
                        "target_metrics": {
                          "max":3410.0,
                          "min":2.0,
                          "std":686.62,
                          "mean":848.17,
                          "type":"numerical",
                          "histogram":{
                             "buckets":[2.0, 342.8, 683.6, 1024.4],
                             "reference_values":[204, 144, 165, 89],
                             "current_values":[123, 231, 122, 89]
                          },
                          "feature_name":"ground_truth",
                          "missing_value":{"count":0, "percentage":0.0},
                          "median_metrics":{"median":713.0, "perc_25":315.0, "perc_75":1097.0}
                        },
                    "featureMetrics": [
                          {
                             "max":731.0,
                             "min":1.0,
                             "std":211.16,
                             "mean":366.0,
                             "type":"numerical",
                             "histogram":{
                                "buckets":[1.0, 74.0, 147.0, 220.0],
                                "reference_values":[73, 73, 73, 73],
                                "current_values":[73, 73, 73, 73]
                             },
                             "feature_name":"instant",
                             "missing_value":{"count":0, "percentage":0.0},
                             "median_metrics":{"median":366.0, "perc_25":183.5, "perc_75":548.5},
                             "class_median_metrics":[]
                          },
                          {
                             "max":4.0,
                             "min":1.0,
                             "std":1.11,
                             "mean":2.49,
                             "type":"numerical",
                             "histogram":{
                                "buckets":[1.0, 1.3, 1.6, 1.9],
                                "reference_values":[181, 0, 0, 184],
                                "current_values":[123, 0, 0, 212]
                             },
                             "feature_name":"season",
                             "missing_value":{"count":0, "percentage":0.0},
                             "median_metrics":{"median":3.0, "perc_25":2.0, "perc_75":3.0},
                             "class_median_metrics":[]
                          },
                          {
                              "type":"categorical",
                              "feature_name":"Sex",
                              "missing_value":{
                                "count":0,
                                "percentage":0.0
                              },
                              "distinct_value":3,
                              "category_frequency":[
                                {
                                  "name":"F",
                                  "count":1064,
                                  "frequency":0.31837223219628963
                                },
                                {
                                  "name":"M",
                                  "count":1208,
                                  "frequency":0.36146020347097546
                                },
                                {
                                  "name":"I",
                                  "count":1070,
                                  "frequency":0.3201675643327349
                                }
                              ]
                          }
                        ]
                    }
                }""",
        )

        metrics = model_current_dataset.data_quality()

        assert isinstance(metrics, RegressionDataQuality)
        assert metrics.n_observations == 731
        assert metrics.target_metrics.feature_name == 'ground_truth'
        assert metrics.target_metrics.median_metrics.median == 713.0
        assert metrics.feature_metrics[0].max == 731.0
        assert metrics.feature_metrics[2].distinct_value == 3
        assert len(metrics.feature_metrics) == 3
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_data_quality_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/data-quality',
            status=200,
            body='{"dataQuality": "wrong"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.data_quality()

    @responses.activate
    def test_data_quality_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/data-quality',
            status=200,
            body='{"wrong": "json"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.data_quality()

    @responses.activate
    def test_binary_class_model_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/model-quality',
            status=200,
            body="""{
                    "datetime": "something_not_used",
                    "jobStatus": "SUCCEEDED",
                    "modelQuality": {
                        "globalMetrics": {
                            "f1": 0.75,
                            "accuracy": 0.90,
                            "precision": 0.88,
                            "recall": 0.87,
                            "fMeasure": 0.85,
                            "weightedPrecision": 0.88,
                            "weightedRecall": 0.87,
                            "weightedFMeasure": 0.85,
                            "weightedTruePositiveRate": 0.90,
                            "weightedFalsePositiveRate": 0.10,
                            "truePositiveRate": 0.87,
                            "falsePositiveRate": 0.13,
                            "truePositiveCount": 870,
                            "falsePositiveCount": 130,
                            "trueNegativeCount": 820,
                            "falseNegativeCount": 180,
                            "areaUnderRoc": 0.92,
                            "areaUnderPr": 0.91
                        },
                        "groupedMetrics": {
                            "f1": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.8},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.85}
                            ],
                            "accuracy": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.88},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.9}
                            ],
                            "precision": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.86},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.88}
                            ],
                            "recall": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.81},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.83}
                            ],
                            "fMeasure": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.8},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.85}
                            ],
                            "weightedPrecision": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.85},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.87}
                            ],
                            "weightedRecall": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.82},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.84}
                            ],
                            "weightedFMeasure": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.84},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.86}
                            ],
                            "weightedTruePositiveRate": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.88},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.9}
                            ],
                            "weightedFalsePositiveRate": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.12},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.1}
                            ],
                            "truePositiveRate": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.81},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.83}
                            ],
                            "falsePositiveRate": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.14},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.12}
                            ],
                            "areaUnderRoc": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.94},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.95}
                            ],
                            "areaUnderPr": [
                                {"timestamp": "2024-01-01T00:00:00Z", "value": 0.91},
                                {"timestamp": "2024-02-01T00:00:00Z", "value": 0.92}
                            ]
                        }
                    }
                }""",
        )

        metrics = model_current_dataset.model_quality()

        assert isinstance(metrics, CurrentBinaryClassificationModelQuality)

        assert metrics.global_metrics.f1 == 0.75
        assert metrics.global_metrics.recall == 0.87
        assert metrics.global_metrics.false_positive_rate == 0.13
        assert metrics.global_metrics.true_negative_count == 820
        assert metrics.global_metrics.area_under_pr == 0.91
        assert len(metrics.grouped_metrics.accuracy) == 2
        assert metrics.grouped_metrics.accuracy[0].value == 0.88
        assert len(metrics.grouped_metrics.area_under_roc) == 2
        assert metrics.grouped_metrics.area_under_roc[1].value == 0.95
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_multi_class_model_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        f1 = 0.75
        accuracy = 0.98
        recall = 0.23
        weighted_precision = 0.15
        weighted_true_positive_rate = 0.01
        weighted_false_positive_rate = 0.23
        weighted_f_measure = 2.45
        true_positive_rate = 4.12
        false_positive_rate = 5.89
        precision = 2.33
        weighted_recall = 4.22
        f_measure = 9.33
        confusion_matrix = [
            [3.0, 0.0, 0.0, 0.0],
            [0.0, 2.0, 1.0, 0.0],
            [0.0, 0.0, 1.0, 2.0],
            [1.0, 0.0, 0.0, 0.0],
        ]
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.MULTI_CLASS,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/model-quality',
            status=200,
            body=f"""{{
                                "datetime": "something_not_used",
                                "jobStatus": "SUCCEEDED",
                                "modelQuality": {{
                                    "classes": ["classA", "classB", "classC", "classD"],
                                    "classMetrics": [
                                        {{
                                            "className": "classA",
                                            "metrics": {{
                                                "accuracy": {accuracy}
                                            }},
                                            "groupedMetrics": {{
                                                    "precision": [
                                                        {{"timestamp": "2024-01-01T00:00:00Z", "value": 0.86}},
                                                        {{"timestamp": "2024-02-01T00:00:00Z", "value": 0.88}}
                                                    ],
                                                    "recall": [
                                                        {{"timestamp": "2024-01-01T00:00:00Z", "value": {recall}}},
                                                        {{"timestamp": "2024-02-01T00:00:00Z", "value": 0.83}}
                                                    ],
                                                    "fMeasure": [
                                                        {{"timestamp": "2024-01-01T00:00:00Z", "value": 0.8}},
                                                        {{"timestamp": "2024-02-01T00:00:00Z", "value": 0.85}}
                                                    ],
                                                    "truePositiveRate": [
                                                        {{"timestamp": "2024-01-01T00:00:00Z", "value": 0.81}},
                                                        {{"timestamp": "2024-02-01T00:00:00Z", "value": 0.83}}
                                                    ],
                                                    "falsePositiveRate": [
                                                        {{"timestamp": "2024-01-01T00:00:00Z", "value": 0.14}},
                                                        {{"timestamp": "2024-02-01T00:00:00Z", "value": 0.12}}
                                                    ]
                                                }}
                                        }},
                                        {{
                                            "className": "classB",
                                            "metrics": {{
                                                "fMeasure": {f_measure}
                                            }}
                                        }},
                                        {{
                                            "className": "classC",
                                            "metrics": {{
                                                "recall": {recall}
                                            }}
                                        }},
                                        {{
                                            "className": "classD",
                                            "metrics": {{
                                                "truePositiveRate": {true_positive_rate},
                                                "falsePositiveRate": {false_positive_rate}
                                            }}
                                        }}
                                    ],
                                    "globalMetrics": {{
                                        "f1": {f1},
                                        "accuracy": {accuracy},
                                        "precision": {precision},
                                        "recall": {recall},
                                        "fMeasure": {f_measure},
                                        "weightedPrecision": {weighted_precision},
                                        "weightedRecall": {weighted_recall},
                                        "weightedFMeasure": {weighted_f_measure},
                                        "weightedTruePositiveRate": {weighted_true_positive_rate},
                                        "weightedFalsePositiveRate": {weighted_false_positive_rate},
                                        "truePositiveRate": {true_positive_rate},
                                        "falsePositiveRate": {false_positive_rate},
                                        "confusionMatrix": {confusion_matrix}
                                    }}
                                }}
                            }}""",
        )

        metrics = model_current_dataset.model_quality()

        assert isinstance(metrics, MultiClassificationModelQuality)
        assert metrics.classes == ['classA', 'classB', 'classC', 'classD']
        assert metrics.global_metrics.accuracy == accuracy
        assert metrics.global_metrics.weighted_precision == weighted_precision
        assert metrics.global_metrics.weighted_recall == weighted_recall
        assert (
            metrics.global_metrics.weighted_true_positive_rate
            == weighted_true_positive_rate
        )
        assert (
            metrics.global_metrics.weighted_false_positive_rate
            == weighted_false_positive_rate
        )
        assert metrics.global_metrics.weighted_f_measure == weighted_f_measure
        assert metrics.global_metrics.true_positive_rate == true_positive_rate
        assert metrics.global_metrics.false_positive_rate == false_positive_rate
        assert metrics.global_metrics.precision == precision
        assert metrics.global_metrics.f_measure == f_measure
        assert metrics.class_metrics[0].class_name == 'classA'
        assert metrics.class_metrics[0].metrics.accuracy == accuracy
        assert metrics.class_metrics[0].grouped_metrics.recall[0].value == recall
        assert metrics.class_metrics[1].class_name == 'classB'
        assert metrics.class_metrics[1].metrics.f_measure == f_measure
        assert metrics.class_metrics[2].class_name == 'classC'
        assert metrics.class_metrics[2].metrics.recall == recall
        assert metrics.class_metrics[3].class_name == 'classD'
        assert (
            metrics.class_metrics[3].metrics.false_positive_rate == false_positive_rate
        )
        assert metrics.class_metrics[3].metrics.true_positive_rate == true_positive_rate
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_regression_model_quality_ok(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.REGRESSION,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/model-quality',
            status=200,
            body="""{
                    "datetime": "something_not_used",
                    "jobStatus": "SUCCEEDED",
                    "modelQuality": {}
                }""",
        )

        metrics = model_current_dataset.model_quality()

        assert isinstance(metrics, CurrentRegressionModelQuality)
        # TODO: add asserts to properties
        assert model_current_dataset.status() == JobStatus.SUCCEEDED

    @responses.activate
    def test_model_quality_validation_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/model-quality',
            status=200,
            body='{"modelQuality": "wrong"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.model_quality()

    @responses.activate
    def test_model_quality_key_error(self):
        base_url = 'http://api:9000'
        model_id = uuid.uuid4()
        import_uuid = uuid.uuid4()
        model_current_dataset = ModelCurrentDataset(
            base_url,
            model_id,
            ModelType.BINARY,
            CurrentFileUpload(
                uuid=import_uuid,
                path='s3://bucket/file.csv',
                date='2014',
                correlation_id_column='column',
                status=JobStatus.IMPORTING,
            ),
        )

        responses.add(
            method=responses.GET,
            url=f'{base_url}/api/models/{str(model_id)}/current/{str(import_uuid)}/model-quality',
            status=200,
            body='{"wrong": "json"}',
        )

        with pytest.raises(ClientError):
            model_current_dataset.model_quality()
