import datetime
import uuid
from pathlib import Path

import deepdiff
import pytest
from pyspark.sql import SparkSession

from jobs.utils.current import CurrentMetricsService
from jobs.utils.models import (
    ModelOut,
    ModelType,
    DataType,
    OutputType,
    ColumnDefinition,
    SupportedTypes,
    Granularity,
)
from jobs.utils.spark import apply_schema_to_dataframe
from tests.utils.pytest_utils import my_approx

test_resource_path = Path(__file__).resolve().parent / "resources"


@pytest.fixture()
def spark_fixture():
    spark = SparkSession.builder.appName("Current PyTest").getOrCreate()
    yield spark


@pytest.fixture()
def dataset(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


@pytest.fixture()
def complete_dataset(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/complete_dataset.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/complete_dataset.csv", header=True
        ),
    )


@pytest.fixture()
def current_joined(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/current_joined.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/reference_joined.csv", header=True
        ),
    )


@pytest.fixture()
def easy_dataset(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/easy_dataset.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/easy_dataset.csv", header=True
        ),
    )


@pytest.fixture()
def dataset_cat_missing(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_cat_missing.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset_cat_missing.csv", header=True
        ),
    )


@pytest.fixture()
def dataset_with_datetime(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_with_datetime.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset_with_datetime.csv", header=True
        ),
    )


@pytest.fixture()
def easy_dataset_bucket_test(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/easy_dataset_bucket_test.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/easy_dataset.csv", header=True
        ),
    )


@pytest.fixture()
def dataset_for_hour(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_for_hour.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


@pytest.fixture()
def dataset_for_day(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_for_day.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


@pytest.fixture()
def dataset_for_week(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_for_week.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


@pytest.fixture()
def dataset_for_month(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_for_month.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


def test_calculation(spark_fixture, dataset):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 4,
        }
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "global_metrics": {
                "f1": 0.901010101010101,
                "accuracy": 0.9,
                "weighted_precision": 0.9199999999999999,
                "weighted_recall": 0.9,
                "weighted_true_positive_rate": 0.9,
                "weighted_false_positive_rate": 0.06666666666666667,
                "weighted_f_measure": 0.901010101010101,
                "true_positive_rate": 0.8333333333333334,
                "false_positive_rate": 0.0,
                "precision": 1.0,
                "recall": 0.8333333333333334,
                "f_measure": 0.9090909090909091,
                "true_positive_count": 5,
                "false_positive_count": 0,
                "true_negative_count": 4,
                "false_negative_count": 1,
                "area_under_roc": 0.41666666666666663,
                "area_under_pr": 0.5652116402116403,
            },
            "grouped_metrics": {
                "f1": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.901010101010101}
                ],
                "accuracy": [{"timestamp": "2024-06-16 00:00:00", "value": 0.9}],
                "weighted_precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.9199999999999999}
                ],
                "weighted_recall": [{"timestamp": "2024-06-16 00:00:00", "value": 0.9}],
                "weighted_true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.9}
                ],
                "weighted_false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.06666666666666667}
                ],
                "weighted_f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.901010101010101}
                ],
                "true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.8333333333333334}
                ],
                "false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                ],
                "precision": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                "recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.8333333333333334}
                ],
                "f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.9090909090909091}
                ],
                "area_under_roc": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.41666666666666663}
                ],
                "area_under_pr": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.5652116402116403}
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "X", "count": 9, "frequency": 0.9},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_current_joined(spark_fixture, current_joined):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="age", type=SupportedTypes.int),
        ColumnDefinition(name="sex", type=SupportedTypes.string),
        ColumnDefinition(name="chest_pain_type", type=SupportedTypes.int),
        ColumnDefinition(name="resting_blood_pressure", type=SupportedTypes.int),
        ColumnDefinition(name="cholesterol", type=SupportedTypes.int),
        ColumnDefinition(name="fasting_blood_sugar", type=SupportedTypes.int),
        ColumnDefinition(name="resting_ecg", type=SupportedTypes.int),
        ColumnDefinition(name="max_heart_rate_achieved", type=SupportedTypes.int),
        ColumnDefinition(name="exercise_induced_angina", type=SupportedTypes.int),
        ColumnDefinition(name="st_depression", type=SupportedTypes.float),
        ColumnDefinition(name="st_slope", type=SupportedTypes.int),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = current_joined
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "categorical": 1,
            "datetime": 1,
            "duplicate_rows": 11,
            "duplicate_rows_perc": 4.621848739495799,
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "n_observations": 238,
            "n_variables": 14,
            "numeric": 12,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 238,
            "class_metrics": [
                {"name": "true", "count": 133, "percentage": 55.88235294117647},
                {"name": "false", "count": 105, "percentage": 44.11764705882353},
            ],
            "feature_metrics": [
                {
                    "feature_name": "age",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 53.34873949579832,
                    "std": 9.050737112869957,
                    "min": 28.0,
                    "max": 74.0,
                    "median_metrics": {
                        "perc_25": 47.0,
                        "median": 54.0,
                        "perc_75": 60.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 54.857142857142854,
                            "median_metrics": {
                                "perc_25": 50.0,
                                "median": 56.0,
                                "perc_75": 60.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 51.43809523809524,
                            "median_metrics": {
                                "perc_25": 45.0,
                                "median": 52.0,
                                "perc_75": 57.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            28.0,
                            32.6,
                            37.2,
                            41.8,
                            46.4,
                            51.0,
                            55.599999999999994,
                            60.199999999999996,
                            64.8,
                            69.4,
                            74.0,
                        ],
                        "reference_values": [4, 7, 14, 29, 26, 59, 48, 23, 24, 4],
                        "current_values": [4, 7, 14, 29, 26, 59, 48, 23, 24, 4],
                    },
                },
                {
                    "feature_name": "chest_pain_type",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 3.235294117647059,
                    "std": 0.9205197793554797,
                    "min": 1.0,
                    "max": 4.0,
                    "median_metrics": {"perc_25": 3.0, "median": 4.0, "perc_75": 4.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 3.6240601503759398,
                            "median_metrics": {
                                "perc_25": 4.0,
                                "median": 4.0,
                                "perc_75": 4.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 2.742857142857143,
                            "median_metrics": {
                                "perc_25": 2.0,
                                "median": 3.0,
                                "perc_75": 3.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.0,
                            1.3,
                            1.6,
                            1.9,
                            2.2,
                            2.5,
                            2.8,
                            3.1,
                            3.4,
                            3.6999999999999997,
                            4.0,
                        ],
                        "reference_values": [12, 0, 0, 43, 0, 0, 60, 0, 0, 123],
                        "current_values": [12, 0, 0, 43, 0, 0, 60, 0, 0, 123],
                    },
                },
                {
                    "feature_name": "resting_blood_pressure",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 132.85294117647058,
                    "std": 18.16286527113178,
                    "min": 94.0,
                    "max": 192.0,
                    "median_metrics": {
                        "perc_25": 120.0,
                        "median": 130.0,
                        "perc_75": 140.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 134.65413533834587,
                            "median_metrics": {
                                "perc_25": 122.0,
                                "median": 131.0,
                                "perc_75": 150.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 130.57142857142858,
                            "median_metrics": {
                                "perc_25": 120.0,
                                "median": 130.0,
                                "perc_75": 140.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            94.0,
                            103.8,
                            113.6,
                            123.4,
                            133.2,
                            143.0,
                            152.8,
                            162.60000000000002,
                            172.4,
                            182.2,
                            192.0,
                        ],
                        "reference_values": [5, 25, 54, 56, 43, 26, 17, 4, 5, 3],
                        "current_values": [5, 25, 54, 56, 43, 26, 17, 4, 5, 3],
                    },
                },
                {
                    "feature_name": "cholesterol",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 212.2436974789916,
                    "std": 107.54541510599883,
                    "min": 0.0,
                    "max": 564.0,
                    "median_metrics": {
                        "perc_25": 186.25,
                        "median": 234.0,
                        "perc_75": 277.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 192.66165413533835,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 230.0,
                                "perc_75": 281.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 237.04761904761904,
                            "median_metrics": {
                                "perc_25": 205.0,
                                "median": 235.0,
                                "perc_75": 275.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.0,
                            56.4,
                            112.8,
                            169.2,
                            225.6,
                            282.0,
                            338.4,
                            394.8,
                            451.2,
                            507.59999999999997,
                            564.0,
                        ],
                        "reference_values": [38, 0, 7, 63, 73, 44, 9, 1, 1, 2],
                        "current_values": [38, 0, 7, 63, 73, 44, 9, 1, 1, 2],
                    },
                },
                {
                    "feature_name": "fasting_blood_sugar",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 0.20588235294117646,
                    "std": 0.4051970646565134,
                    "min": 0.0,
                    "max": 1.0,
                    "median_metrics": {"perc_25": 0.0, "median": 0.0, "perc_75": 0.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.3082706766917293,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.0761904761904762,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 0.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.0,
                            0.1,
                            0.2,
                            0.30000000000000004,
                            0.4,
                            0.5,
                            0.6000000000000001,
                            0.7000000000000001,
                            0.8,
                            0.9,
                            1.0,
                        ],
                        "reference_values": [189, 0, 0, 0, 0, 0, 0, 0, 0, 49],
                        "current_values": [189, 0, 0, 0, 0, 0, 0, 0, 0, 49],
                    },
                },
                {
                    "feature_name": "resting_ecg",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 0.7016806722689075,
                    "std": 0.8710518587532667,
                    "min": 0.0,
                    "max": 2.0,
                    "median_metrics": {"perc_25": 0.0, "median": 0.0, "perc_75": 2.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.7218045112781954,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 2.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.6761904761904762,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 2.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.0,
                            0.2,
                            0.4,
                            0.6000000000000001,
                            0.8,
                            1.0,
                            1.2000000000000002,
                            1.4000000000000001,
                            1.6,
                            1.8,
                            2.0,
                        ],
                        "reference_values": [136, 0, 0, 0, 0, 37, 0, 0, 0, 65],
                        "current_values": [136, 0, 0, 0, 0, 37, 0, 0, 0, 65],
                    },
                },
                {
                    "feature_name": "max_heart_rate_achieved",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 138.84453781512605,
                    "std": 26.31962319212335,
                    "min": 63.0,
                    "max": 195.0,
                    "median_metrics": {
                        "perc_25": 120.0,
                        "median": 140.0,
                        "perc_75": 159.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 128.54135338345864,
                            "median_metrics": {
                                "perc_25": 112.0,
                                "median": 128.0,
                                "perc_75": 145.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 151.89523809523808,
                            "median_metrics": {
                                "perc_25": 140.0,
                                "median": 155.0,
                                "perc_75": 165.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            63.0,
                            76.2,
                            89.4,
                            102.6,
                            115.8,
                            129.0,
                            142.2,
                            155.39999999999998,
                            168.6,
                            181.8,
                            195.0,
                        ],
                        "reference_values": [3, 5, 16, 22, 41, 38, 43, 37, 23, 10],
                        "current_values": [3, 5, 16, 22, 41, 38, 43, 37, 23, 10],
                    },
                },
                {
                    "feature_name": "exercise_induced_angina",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 0.42857142857142855,
                    "std": 0.4959145933585413,
                    "min": 0.0,
                    "max": 1.0,
                    "median_metrics": {"perc_25": 0.0, "median": 0.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.6616541353383458,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.13333333333333333,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 0.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.0,
                            0.1,
                            0.2,
                            0.30000000000000004,
                            0.4,
                            0.5,
                            0.6000000000000001,
                            0.7000000000000001,
                            0.8,
                            0.9,
                            1.0,
                        ],
                        "reference_values": [136, 0, 0, 0, 0, 0, 0, 0, 0, 102],
                        "current_values": [136, 0, 0, 0, 0, 0, 0, 0, 0, 102],
                    },
                },
                {
                    "feature_name": "st_depression",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 0.9920168067226889,
                    "std": 1.0415317183799289,
                    "min": -1.1,
                    "max": 4.0,
                    "median_metrics": {
                        "perc_25": 0.0,
                        "median": 1.0,
                        "perc_75": 1.6749999999999998,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4180451127819549,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 1.4,
                                "perc_75": 2.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.4523809523809524,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 1.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -1.1,
                            -0.5900000000000001,
                            -0.08000000000000007,
                            0.42999999999999994,
                            0.94,
                            1.4499999999999997,
                            1.96,
                            2.47,
                            2.98,
                            3.4899999999999998,
                            4.0,
                        ],
                        "reference_values": [2, 1, 97, 17, 40, 32, 19, 15, 12, 3],
                        "current_values": [2, 1, 97, 17, 40, 32, 19, 15, 12, 3],
                    },
                },
                {
                    "feature_name": "st_slope",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 1.6428571428571428,
                    "std": 0.5905116752253559,
                    "min": 1.0,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 2.0, "perc_75": 2.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.9323308270676691,
                            "median_metrics": {
                                "perc_25": 2.0,
                                "median": 2.0,
                                "perc_75": 2.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 1.276190476190476,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.0,
                            1.2,
                            1.4,
                            1.6,
                            1.8,
                            2.0,
                            2.2,
                            2.4000000000000004,
                            2.6,
                            2.8,
                            3.0,
                        ],
                        "reference_values": [99, 0, 0, 0, 0, 125, 0, 0, 0, 14],
                        "current_values": [99, 0, 0, 0, 0, 125, 0, 0, 0, 14],
                    },
                },
                {
                    "feature_name": "sex",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "F", "count": 49, "frequency": 0.20588235294117646},
                        {"name": "M", "count": 189, "frequency": 0.7941176470588235},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_complete(spark_fixture, complete_dataset):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.bool)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = complete_dataset
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 7,
            "n_observations": 7,
            "numeric": 4,
            "categorical": 2,
            "datetime": 1,
        },
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 7,
            "class_metrics": [
                {"name": "true", "count": 7, "percentage": 100.0},
                {"name": "false", "count": 0, "percentage": 0.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 1.0,
                    "std": 0.0,
                    "min": 1.0,
                    "max": 1.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.0,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.0,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 0.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [1.0, 1.0],
                        "reference_values": [7],
                        "current_values": [7],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 100.0,
                    "std": 0.0,
                    "min": 100.0,
                    "max": 100.0,
                    "median_metrics": {
                        "perc_25": 100.0,
                        "median": 100.0,
                        "perc_75": 100.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 100.0,
                            "median_metrics": {
                                "perc_25": 100.0,
                                "median": 100.0,
                                "perc_75": 100.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.0,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 0.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [100.0, 100.0],
                        "reference_values": [7],
                        "current_values": [7],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "B", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "C", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "D", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "E", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "F", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "G", "count": 1, "frequency": 0.14285714285714285},
                    ],
                    "distinct_value": 7,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "B", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "C", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "D", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "E", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "F", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "G", "count": 1, "frequency": 0.14285714285714285},
                    ],
                    "distinct_value": 7,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_easy_dataset(spark_fixture, easy_dataset):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = easy_dataset
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 7,
            "n_observations": 7,
            "numeric": 4,
            "categorical": 2,
            "datetime": 1,
        },
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 7,
            "class_metrics": [
                {"name": "true", "count": 6, "percentage": 85.71428571428571},
                {"name": "false", "count": 1, "percentage": 14.285714285714285},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 1.0,
                    "std": 0.0,
                    "min": 1.0,
                    "max": 1.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.0,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 1.0,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [1.0, 1.0],
                        "reference_values": [7],
                        "current_values": [7],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 100.0,
                    "std": 0.0,
                    "min": 100.0,
                    "max": 100.0,
                    "median_metrics": {
                        "perc_25": 100.0,
                        "median": 100.0,
                        "perc_75": 100.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 100.0,
                            "median_metrics": {
                                "perc_25": 100.0,
                                "median": 100.0,
                                "perc_75": 100.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 100.0,
                            "median_metrics": {
                                "perc_25": 100.0,
                                "median": 100.0,
                                "perc_75": 100.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [100.0, 100.0],
                        "reference_values": [7],
                        "current_values": [7],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "B", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "C", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "D", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "E", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "F", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "G", "count": 1, "frequency": 0.14285714285714285},
                    ],
                    "distinct_value": 7,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "B", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "C", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "D", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "E", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "F", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "G", "count": 1, "frequency": 0.14285714285714285},
                    ],
                    "distinct_value": 7,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_cat_missing(spark_fixture, dataset_cat_missing):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset_cat_missing
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 5,
            "missing_cells_perc": 7.142857142857142,
            "duplicate_rows": 2,
            "duplicate_rows_perc": 20.0,
            "n_variables": 7,
            "n_observations": 10,
            "numeric": 4,
            "categorical": 2,
            "datetime": 1,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 3, "frequency": 0.3},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "category_frequency": [
                        {"name": "X", "count": 8, "frequency": 0.8},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_with_datetime(spark_fixture, dataset_with_datetime):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset_with_datetime
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 4,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "X", "count": 9, "frequency": 0.9},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_easy_dataset_bucket_test(spark_fixture, easy_dataset_bucket_test):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = easy_dataset_bucket_test
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 7,
            "n_observations": 7,
            "numeric": 4,
            "categorical": 2,
            "datetime": 1,
        },
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 7,
            "class_metrics": [
                {"name": "true", "count": 6, "percentage": 85.71428571428571},
                {"name": "false", "count": 1, "percentage": 14.285714285714285},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": -1.1428571428571429e-05,
                    "std": 3.7796447300922724e-06,
                    "min": -2e-05,
                    "max": -1e-05,
                    "median_metrics": {
                        "perc_25": -1e-05,
                        "median": -1e-05,
                        "perc_75": -1e-05,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": -1.1666666666666668e-05,
                            "median_metrics": {
                                "perc_25": -1e-05,
                                "median": -1e-05,
                                "perc_75": -1e-05,
                            },
                        },
                        {
                            "name": "false",
                            "mean": -1e-05,
                            "median_metrics": {
                                "perc_25": -1e-05,
                                "median": -1e-05,
                                "perc_75": -1e-05,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -2e-05,
                            0.09998199999999999,
                            0.199984,
                            0.299986,
                            0.39998799999999995,
                            0.49998999999999993,
                            0.599992,
                            0.6999939999999999,
                            0.7999959999999999,
                            0.899998,
                            1.0,
                        ],
                        "reference_values": [0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                        "current_values": [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "mean": 100.00000014285715,
                    "std": 3.779644720549587e-07,
                    "min": 100.0,
                    "max": 100.000001,
                    "median_metrics": {
                        "perc_25": 100.0,
                        "median": 100.0,
                        "perc_75": 100.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 100.00000016666667,
                            "median_metrics": {
                                "perc_25": 100.0,
                                "median": 100.0,
                                "perc_75": 100.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 100.0,
                            "median_metrics": {
                                "perc_25": 100.0,
                                "median": 100.0,
                                "perc_75": 100.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            100.0,
                            100.0000001,
                            100.0000002,
                            100.0000003,
                            100.0000004,
                            100.0000005,
                            100.00000059999999,
                            100.0000007,
                            100.0000008,
                            100.0000009,
                            100.000001,
                        ],
                        "reference_values": [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        "current_values": [6, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "B", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "C", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "D", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "E", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "F", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "G", "count": 1, "frequency": 0.14285714285714285},
                    ],
                    "distinct_value": 7,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "B", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "C", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "D", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "E", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "F", "count": 1, "frequency": 0.14285714285714285},
                        {"name": "G", "count": 1, "frequency": 0.14285714285714285},
                    ],
                    "distinct_value": 7,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_hour(spark_fixture, dataset_for_hour):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset_for_hour
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 4,
        }
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "global_metrics": {
                "f1": 0.901010101010101,
                "accuracy": 0.9,
                "weighted_precision": 0.9199999999999999,
                "weighted_recall": 0.9,
                "weighted_true_positive_rate": 0.9,
                "weighted_false_positive_rate": 0.06666666666666667,
                "weighted_f_measure": 0.901010101010101,
                "true_positive_rate": 0.8333333333333334,
                "false_positive_rate": 0.0,
                "precision": 1.0,
                "recall": 0.8333333333333334,
                "f_measure": 0.9090909090909091,
                "true_positive_count": 5,
                "false_positive_count": 0,
                "true_negative_count": 4,
                "false_negative_count": 1,
                "area_under_roc": 0.41666666666666663,
                "area_under_pr": 0.5652116402116403,
            },
            "grouped_metrics": {
                "f1": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.5333333333333333},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "accuracy": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "weighted_precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.4444444444444444},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "weighted_recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "weighted_true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "weighted_false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                ],
                "weighted_f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.5333333333333333},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                ],
                "precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "area_under_roc": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 01:00:00", "value": 0.5},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
                "area_under_pr": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.25},
                    {"timestamp": "2024-06-16 01:00:00", "value": 0.5},
                    {"timestamp": "2024-06-16 02:00:00", "value": 0.16666666666666666},
                    {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                    {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "X", "count": 9, "frequency": 0.9},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_day(spark_fixture, dataset_for_day):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.DAY
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset_for_day
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 4,
        }
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "global_metrics": {
                "f1": 0.901010101010101,
                "accuracy": 0.9,
                "weighted_precision": 0.9199999999999999,
                "weighted_recall": 0.9,
                "weighted_true_positive_rate": 0.9,
                "weighted_false_positive_rate": 0.06666666666666667,
                "weighted_f_measure": 0.901010101010101,
                "true_positive_rate": 0.8333333333333334,
                "false_positive_rate": 0.0,
                "precision": 1.0,
                "recall": 0.8333333333333334,
                "f_measure": 0.9090909090909091,
                "true_positive_count": 5,
                "false_positive_count": 0,
                "true_negative_count": 4,
                "false_negative_count": 1,
                "area_under_roc": 0.41666666666666663,
                "area_under_pr": 0.5652116402116403,
            },
            "grouped_metrics": {
                "f1": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.5333333333333333},
                    {"timestamp": "2024-06-18 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "accuracy": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-18 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "weighted_precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.4444444444444444},
                    {"timestamp": "2024-06-18 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "weighted_recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-18 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "weighted_true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-18 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "weighted_false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-06-18 00:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-19 00:00:00", "value": float("nan")},
                ],
                "weighted_f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.5333333333333333},
                    {"timestamp": "2024-06-18 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-18 00:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-18 00:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-19 00:00:00", "value": float("nan")},
                ],
                "precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-18 00:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-18 00:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-18 00:00:00", "value": float("nan")},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "area_under_roc": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.5},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-18 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
                "area_under_pr": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.7916666666666666},
                    {"timestamp": "2024-06-17 00:00:00", "value": 0.16666666666666666},
                    {"timestamp": "2024-06-18 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-19 00:00:00", "value": 1.0},
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "X", "count": 9, "frequency": 0.9},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_week(spark_fixture, dataset_for_week):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.WEEK
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset_for_week
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 4,
        }
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "global_metrics": {
                "f1": 0.901010101010101,
                "accuracy": 0.9,
                "weighted_precision": 0.9199999999999999,
                "weighted_recall": 0.9,
                "weighted_true_positive_rate": 0.9,
                "weighted_false_positive_rate": 0.06666666666666667,
                "weighted_f_measure": 0.901010101010101,
                "true_positive_rate": 0.8333333333333334,
                "false_positive_rate": 0.0,
                "precision": 1.0,
                "recall": 0.8333333333333334,
                "f_measure": 0.9090909090909091,
                "true_positive_count": 5,
                "false_positive_count": 0,
                "true_negative_count": 4,
                "false_negative_count": 1,
                "area_under_roc": 0.41666666666666663,
                "area_under_pr": 0.5652116402116403,
            },
            "grouped_metrics": {
                "f1": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.7666666666666667},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "accuracy": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.75},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "weighted_precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.875},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "weighted_recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.75},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "weighted_true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.75},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "weighted_false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.08333333333333333},
                    {"timestamp": "2024-07-14 00:00:00", "value": float("nan")},
                ],
                "weighted_f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.7666666666666667},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "true_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "false_positive_rate": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.0},
                    {"timestamp": "2024-07-14 00:00:00", "value": float("nan")},
                ],
                "precision": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "recall": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "f_measure": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 1.0},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.8},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "area_under_roc": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                    {"timestamp": "2024-06-23 00:00:00", "value": 0.5},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.3333333333333333},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
                "area_under_pr": [
                    {"timestamp": "2024-06-16 00:00:00", "value": 0.16666666666666666},
                    {"timestamp": "2024-06-23 00:00:00", "value": 0.5},
                    {"timestamp": "2024-06-30 00:00:00", "value": 0.6805555555555556},
                    {"timestamp": "2024-07-14 00:00:00", "value": 1.0},
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "X", "count": 9, "frequency": 0.9},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_month(spark_fixture, dataset_for_month):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataset, reference_dataset = dataset_for_month
    current_dataset = apply_schema_to_dataframe(
        current_dataset, model.to_current_spark_schema()
    )
    current_dataset = current_dataset.select(
        *[
            c
            for c in model.to_current_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    reference_dataset = apply_schema_to_dataframe(
        reference_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in current_dataset.columns
        ]
    )
    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        model=model,
    )
    stats = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 4,
        }
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "global_metrics": {
                "f1": 0.901010101010101,
                "accuracy": 0.9,
                "weighted_precision": 0.9199999999999999,
                "weighted_recall": 0.9,
                "weighted_true_positive_rate": 0.9,
                "weighted_false_positive_rate": 0.06666666666666667,
                "weighted_f_measure": 0.901010101010101,
                "true_positive_rate": 0.8333333333333334,
                "false_positive_rate": 0.0,
                "precision": 1.0,
                "recall": 0.8333333333333334,
                "f_measure": 0.9090909090909091,
                "true_positive_count": 5,
                "false_positive_count": 0,
                "true_negative_count": 4,
                "false_negative_count": 1,
                "area_under_roc": 0.41666666666666663,
                "area_under_pr": 0.5652116402116403,
            },
            "grouped_metrics": {
                "f1": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.5333333333333333},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "accuracy": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "weighted_precision": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.4444444444444444},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "weighted_recall": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "weighted_true_positive_rate": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "weighted_false_positive_rate": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.6666666666666666},
                    {"timestamp": "2024-08-01 00:00:00", "value": float("nan")},
                ],
                "weighted_f_measure": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.5333333333333333},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "true_positive_rate": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "false_positive_rate": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-08-01 00:00:00", "value": float("nan")},
                ],
                "precision": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "recall": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "f_measure": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 1.0},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "area_under_roc": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 0.375},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.0},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
                "area_under_pr": [
                    {"timestamp": "2024-06-01 00:00:00", "value": 0.4583333333333333},
                    {"timestamp": "2024-07-01 00:00:00", "value": 0.16666666666666666},
                    {"timestamp": "2024-08-01 00:00:00", "value": 1.0},
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "true", "count": 5, "percentage": 50.0},
                {"name": "false", "count": 5, "percentage": 50.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.7500000000000001,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 1.4,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.875,
                            "median_metrics": {
                                "perc_25": 0.5,
                                "median": 0.75,
                                "perc_75": 1.125,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            0.5,
                            0.75,
                            1.0,
                            1.25,
                            1.5,
                            1.75,
                            2.0,
                            2.25,
                            2.5,
                            2.75,
                            3.0,
                        ],
                        "reference_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                        "current_values": [2, 0, 5, 0, 1, 0, 0, 0, 0, 1],
                    },
                },
                {
                    "feature_name": "num2",
                    "type": "numerical",
                    "missing_value": {"count": 2, "percentage": 20.0},
                    "mean": 277.675,
                    "std": 201.88635947695215,
                    "min": 1.4,
                    "max": 499.0,
                    "median_metrics": {
                        "perc_25": 117.25,
                        "median": 250.0,
                        "perc_75": 499.0,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 324.28000000000003,
                            "median_metrics": {
                                "perc_25": 123.0,
                                "median": 499.0,
                                "perc_75": 499.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 200.0,
                            "median_metrics": {
                                "perc_25": 150.0,
                                "median": 200.0,
                                "perc_75": 250.0,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            1.4,
                            51.160000000000004,
                            100.92000000000002,
                            150.68000000000004,
                            200.44000000000003,
                            250.20000000000002,
                            299.96000000000004,
                            349.72,
                            399.48,
                            449.24,
                            499.0,
                        ],
                        "reference_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                        "current_values": [1, 1, 1, 1, 0, 0, 1, 0, 0, 3],
                    },
                },
                {
                    "feature_name": "cat1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "A", "count": 5, "frequency": 0.5},
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "X", "count": 9, "frequency": 0.9},
                        {"name": "Y", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )
