import datetime
import uuid
from pathlib import Path

import deepdiff

import pytest
from pyspark.sql import SparkSession

from jobs.utils.models import (
    ModelOut,
    ModelType,
    DataType,
    OutputType,
    ColumnDefinition,
    SupportedTypes,
    Granularity,
)
from jobs.utils.reference import ReferenceMetricsService
from jobs.utils.spark import apply_schema_to_dataframe
from tests.utils.pytest_utils import my_approx

test_resource_path = Path(__file__).resolve().parent / "resources"


@pytest.fixture()
def spark_fixture():
    spark = SparkSession.builder.appName("Reference PyTest").getOrCreate()
    yield spark


@pytest.fixture()
def dataset(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/dataset.csv", header=True
    )


@pytest.fixture()
def complete_dataset(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/complete_dataset.csv", header=True
    )


@pytest.fixture()
def reference_joined(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/reference_joined.csv", header=True
    )


@pytest.fixture()
def easy_dataset(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/easy_dataset.csv", header=True
    )


@pytest.fixture()
def dataset_cat_missing(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/dataset_cat_missing.csv", header=True
    )


@pytest.fixture()
def dataset_with_datetime(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/dataset_with_datetime.csv", header=True
    )


@pytest.fixture()
def enhanced_data(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/enhanced_data.csv", header=True
    )


@pytest.fixture()
def dataset_bool_missing(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/dataset_bool_missing.csv", header=True
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

    reference_dataset = apply_schema_to_dataframe(
        dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)

    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 3.75,
            "n_observations": 10,
            "n_variables": 8,
            "numeric": 5,
        }
    )
    assert model_quality == my_approx(
        {
            "accuracy": 0.9,
            "area_under_pr": 0.5652116402116403,
            "area_under_roc": 0.41666666666666663,
            "f1": 0.901010101010101,
            "f_measure": 0.9090909090909091,
            "false_positive_rate": 0.0,
            "precision": 1.0,
            "recall": 0.8333333333333334,
            "true_positive_rate": 0.8333333333333334,
            "weighted_f_measure": 0.901010101010101,
            "weighted_false_positive_rate": 0.06666666666666667,
            "weighted_precision": 0.9199999999999999,
            "weighted_recall": 0.9,
            "weighted_true_positive_rate": 0.9,
            "true_positive_count": 5,
            "false_positive_count": 0,
            "true_negative_count": 4,
            "false_negative_count": 1,
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
                            "mean": 303.56666666666666,
                            "median_metrics": {
                                "perc_25": 142.25,
                                "median": 349.5,
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


def test_calculation_reference_joined(spark_fixture, reference_joined):
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

    reference_dataset = apply_schema_to_dataframe(
        reference_joined, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )

    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
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
            "n_variables": 15,
            "numeric": 13,
        }
    )
    assert model_quality == my_approx(
        {
            "accuracy": 0.9495798319327731,
            "area_under_pr": 0.48119821761196413,
            "area_under_roc": 0.4314403938075195,
            "f1": 0.949532986436427,
            "f_measure": 0.9545454545454546,
            "false_positive_rate": 0.06542056074766354,
            "precision": 0.9473684210526315,
            "recall": 0.9618320610687023,
            "true_positive_rate": 0.9618320610687023,
            "weighted_f_measure": 0.949532986436427,
            "weighted_false_positive_rate": 0.053168331611734364,
            "weighted_precision": 0.9496219540447758,
            "weighted_recall": 0.9495798319327731,
            "weighted_true_positive_rate": 0.9495798319327731,
            "true_positive_count": 126,
            "false_positive_count": 7,
            "true_negative_count": 100,
            "false_negative_count": 5,
        },
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
                            "mean": 54.85496183206107,
                            "median_metrics": {
                                "perc_25": 50.0,
                                "median": 56.0,
                                "perc_75": 60.5,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 51.504672897196265,
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
                            "mean": 3.6106870229007635,
                            "median_metrics": {
                                "perc_25": 4.0,
                                "median": 4.0,
                                "perc_75": 4.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 2.7757009345794392,
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
                            "mean": 134.55725190839695,
                            "median_metrics": {
                                "perc_25": 120.0,
                                "median": 130.0,
                                "perc_75": 145.5,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 130.7663551401869,
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
                            "mean": 193.2290076335878,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 237.0,
                                "perc_75": 281.5,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 235.52336448598132,
                            "median_metrics": {
                                "perc_25": 202.0,
                                "median": 231.0,
                                "perc_75": 273.0,
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
                            "mean": 0.2900763358778626,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.102803738317757,
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
                            "mean": 0.7557251908396947,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 0.0,
                                "perc_75": 2.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.6355140186915887,
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
                            "mean": 129.25954198473283,
                            "median_metrics": {
                                "perc_25": 112.0,
                                "median": 128.0,
                                "perc_75": 146.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 150.57943925233644,
                            "median_metrics": {
                                "perc_25": 138.0,
                                "median": 154.0,
                                "perc_75": 164.5,
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
                            "mean": 0.6564885496183206,
                            "median_metrics": {
                                "perc_25": 0.0,
                                "median": 1.0,
                                "perc_75": 1.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.14953271028037382,
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
                            "mean": 1.3854961832061068,
                            "median_metrics": {
                                "perc_25": 0.30000000000000004,
                                "median": 1.4,
                                "perc_75": 2.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.5102803738317757,
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
                            "mean": 1.900763358778626,
                            "median_metrics": {
                                "perc_25": 2.0,
                                "median": 2.0,
                                "perc_75": 2.0,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 1.3271028037383177,
                            "median_metrics": {
                                "perc_25": 1.0,
                                "median": 1.0,
                                "perc_75": 2.0,
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

    reference_dataset = apply_schema_to_dataframe(
        complete_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 8,
            "n_observations": 7,
            "numeric": 4,
            "categorical": 3,
            "datetime": 1,
        },
    )

    assert model_quality == my_approx(
        {
            "accuracy": 1.0,
            "area_under_pr": 1.0,
            "area_under_roc": 1.0,
            "f1": 1.0,
            "f_measure": 1.0,
            "false_positive_rate": float("nan"),
            "precision": 1.0,
            "recall": 1.0,
            "true_positive_rate": 1.0,
            "weighted_f_measure": 1.0,
            "weighted_false_positive_rate": float("nan"),
            "weighted_precision": 1.0,
            "weighted_recall": 1.0,
            "weighted_true_positive_rate": 1.0,
            "true_positive_count": 7,
            "false_positive_count": 0,
            "true_negative_count": 0,
            "false_negative_count": 0,
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
                    "histogram": {"buckets": [1.0, 1.0], "reference_values": [7]},
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
                    "histogram": {"buckets": [100.0, 100.0], "reference_values": [7]},
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

    reference_dataset = apply_schema_to_dataframe(
        easy_dataset, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 8,
            "n_observations": 7,
            "numeric": 5,
            "categorical": 2,
            "datetime": 1,
        },
    )
    assert model_quality == my_approx(
        {
            "area_under_roc": 0.5,
            "area_under_pr": 0.8571428571428572,
            "f1": 0.7142857142857143,
            "accuracy": 0.7142857142857143,
            "weighted_precision": 0.7142857142857143,
            "weighted_recall": 0.7142857142857143,
            "weighted_true_positive_rate": 0.7142857142857143,
            "weighted_false_positive_rate": 0.8809523809523809,
            "weighted_f_measure": 0.7142857142857143,
            "true_positive_rate": 0.8333333333333334,
            "false_positive_rate": 1.0,
            "precision": 0.8333333333333334,
            "recall": 0.8333333333333334,
            "f_measure": 0.8333333333333334,
            "true_positive_count": 5,
            "false_positive_count": 1,
            "true_negative_count": 0,
            "false_negative_count": 1,
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
                    "histogram": {"buckets": [1.0, 1.0], "reference_values": [7]},
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
                    "histogram": {"buckets": [100.0, 100.0], "reference_values": [7]},
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

    reference_dataset = apply_schema_to_dataframe(
        dataset_cat_missing, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 5,
            "missing_cells_perc": 6.25,
            "duplicate_rows": 2,
            "duplicate_rows_perc": 20.0,
            "n_variables": 8,
            "n_observations": 10,
            "numeric": 5,
            "categorical": 2,
            "datetime": 1,
        }
    )
    assert model_quality == my_approx(
        {
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
                            "mean": 303.56666666666666,
                            "median_metrics": {
                                "perc_25": 142.25,
                                "median": 349.5,
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

    reference_dataset = apply_schema_to_dataframe(
        dataset_with_datetime, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 3,
            "duplicate_rows_perc": 30.0,
            "missing_cells": 3,
            "missing_cells_perc": 3.75,
            "n_observations": 10,
            "n_variables": 8,
            "numeric": 5,
        }
    )
    assert model_quality == my_approx(
        {
            "accuracy": 0.9,
            "area_under_pr": 0.5652116402116403,
            "area_under_roc": 0.41666666666666663,
            "f1": 0.901010101010101,
            "f_measure": 0.9090909090909091,
            "false_positive_rate": 0.0,
            "precision": 1.0,
            "recall": 0.8333333333333334,
            "true_positive_rate": 0.8333333333333334,
            "weighted_f_measure": 0.901010101010101,
            "weighted_false_positive_rate": 0.06666666666666667,
            "weighted_precision": 0.9199999999999999,
            "weighted_recall": 0.9,
            "weighted_true_positive_rate": 0.9,
            "true_positive_count": 5,
            "false_positive_count": 0,
            "true_negative_count": 4,
            "false_negative_count": 1,
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
                            "mean": 303.56666666666666,
                            "median_metrics": {
                                "perc_25": 142.25,
                                "median": 349.5,
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


def test_calculation_enhanced_data(spark_fixture, enhanced_data):
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
        ColumnDefinition(name="feature_0", type=SupportedTypes.float),
        ColumnDefinition(name="feature_1", type=SupportedTypes.float),
        ColumnDefinition(name="feature_2", type=SupportedTypes.float),
        ColumnDefinition(name="feature_3", type=SupportedTypes.float),
        ColumnDefinition(name="feature_4", type=SupportedTypes.float),
        ColumnDefinition(name="feature_5", type=SupportedTypes.float),
        ColumnDefinition(name="feature_6", type=SupportedTypes.float),
        ColumnDefinition(name="feature_7", type=SupportedTypes.float),
        ColumnDefinition(name="feature_8", type=SupportedTypes.float),
        ColumnDefinition(name="feature_9", type=SupportedTypes.float),
        ColumnDefinition(name="cat_1", type=SupportedTypes.string),
        ColumnDefinition(name="cat_2", type=SupportedTypes.string),
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

    reference_dataset = apply_schema_to_dataframe(
        enhanced_data, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)

    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 2996,
            "missing_cells_perc": 0.6241666666666668,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 16,
            "n_observations": 30000,
            "numeric": 13,
            "categorical": 2,
            "datetime": 1,
        }
    )
    assert model_quality == my_approx(
        {
            "f1": 0.33436585801489166,
            "accuracy": 0.49983333333333335,
            "weighted_precision": 0.7502755141767055,
            "weighted_recall": 0.4998333333333333,
            "weighted_true_positive_rate": 0.4998333333333333,
            "weighted_false_positive_rate": 0.49763889258323357,
            "weighted_f_measure": 0.33436585801489166,
            "true_positive_rate": 1.0,
            "false_positive_rate": 0.9978055592499002,
            "precision": 0.4992825441318784,
            "recall": 1.0,
            "f_measure": 0.6660286229384139,
            "true_positive_count": 14962,
            "false_positive_count": 15005,
            "true_negative_count": 33,
            "false_negative_count": 0,
            "area_under_roc": 0.4979357845301016,
            "area_under_pr": 0.24960748683012762,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 30000,
            "class_metrics": [
                {"name": "true", "count": 29967, "percentage": 99.89},
                {"name": "false", "count": 33, "percentage": 0.11},
            ],
            "feature_metrics": [
                {
                    "feature_name": "feature_0",
                    "type": "numerical",
                    "missing_value": {"count": 306, "percentage": 1.02},
                    "mean": -0.19787382089724936,
                    "std": 1.5851074081724228,
                    "min": -8.922759660331181,
                    "max": 9.024875913426545,
                    "median_metrics": {
                        "perc_25": -1.0840126970135682,
                        "median": -0.2502794169949083,
                        "perc_75": 0.5933410153121773,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": -0.37506960472853207,
                            "median_metrics": {
                                "perc_25": -1.2609072304317717,
                                "median": -0.43833821174033677,
                                "perc_75": 0.46427841798865066,
                            },
                        },
                        {
                            "name": "false",
                            "mean": -0.021559015835350998,
                            "median_metrics": {
                                "perc_25": -0.8598675216604383,
                                "median": -0.09580214279499416,
                                "perc_75": 0.7159447439762198,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -8.922759660331181,
                            -7.127996102955408,
                            -5.333232545579635,
                            -3.5384689882038636,
                            -1.7437054308280908,
                            0.05105812654768194,
                            1.8458216839234538,
                            3.6405852412992274,
                            5.435348798674999,
                            7.230112356050771,
                            9.024875913426545,
                        ],
                        "reference_values": [
                            9,
                            64,
                            533,
                            3223,
                            13998,
                            9227,
                            2033,
                            504,
                            92,
                            11,
                        ],
                    },
                },
                {
                    "feature_name": "feature_1",
                    "type": "numerical",
                    "missing_value": {"count": 297, "percentage": 0.9900000000000001},
                    "mean": -0.0921695488550968,
                    "std": 1.4371077194777786,
                    "min": -7.071323418123159,
                    "max": 7.342346103893297,
                    "median_metrics": {
                        "perc_25": -1.01949325701271,
                        "median": -0.0766183061333018,
                        "perc_75": 0.8552504712786367,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": -0.40811487005765135,
                            "median_metrics": {
                                "perc_25": -1.2309347077271604,
                                "median": -0.4125170988265542,
                                "perc_75": 0.4025774318708635,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.22298962729806326,
                            "median_metrics": {
                                "perc_25": -0.6827289123206155,
                                "median": 0.3448547892578119,
                                "perc_75": 1.2488688828393162,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -7.071323418123159,
                            -5.629956465921513,
                            -4.188589513719868,
                            -2.747222561518223,
                            -1.305855609316577,
                            0.13551134288506894,
                            1.576878295086713,
                            3.018245247288359,
                            4.459612199490005,
                            5.900979151691651,
                            7.342346103893297,
                        ],
                        "reference_values": [
                            15,
                            119,
                            878,
                            4695,
                            10859,
                            9741,
                            2935,
                            408,
                            47,
                            6,
                        ],
                    },
                },
                {
                    "feature_name": "feature_2",
                    "type": "numerical",
                    "missing_value": {"count": 311, "percentage": 1.0366666666666666},
                    "mean": -0.024992875662421823,
                    "std": 1.95859549503405,
                    "min": -7.484849550803829,
                    "max": 7.714737509385212,
                    "median_metrics": {
                        "perc_25": -1.447157073352852,
                        "median": -0.1423515033878019,
                        "perc_75": 1.2966669810036546,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": -0.2564646946478202,
                            "median_metrics": {
                                "perc_25": -1.663119039313509,
                                "median": -0.4597462024125228,
                                "perc_75": 1.0674457857547113,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.20549865799116152,
                            "median_metrics": {
                                "perc_25": -1.16217715339232,
                                "median": 0.14058761360269711,
                                "perc_75": 1.519086791402387,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -7.484849550803829,
                            -5.964890844784925,
                            -4.444932138766021,
                            -2.924973432747117,
                            -1.4050147267282123,
                            0.11494397929069233,
                            1.6349026853095951,
                            3.1548613913284997,
                            4.674820097347404,
                            6.194778803366309,
                            7.714737509385212,
                        ],
                        "reference_values": [
                            10,
                            159,
                            1512,
                            5953,
                            8667,
                            7357,
                            4235,
                            1454,
                            315,
                            27,
                        ],
                    },
                },
                {
                    "feature_name": "feature_3",
                    "type": "numerical",
                    "missing_value": {"count": 289, "percentage": 0.9633333333333334},
                    "mean": 0.24629604942463051,
                    "std": 1.487640839531391,
                    "min": -5.924351030623907,
                    "max": 5.895536826775548,
                    "median_metrics": {
                        "perc_25": -0.7248317693310871,
                        "median": 0.2917484210629673,
                        "perc_75": 1.2565657381789663,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.018757699661252642,
                            "median_metrics": {
                                "perc_25": -1.00041187394906,
                                "median": 0.06304933415520031,
                                "perc_75": 1.0905205627020491,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.4725666484307847,
                            "median_metrics": {
                                "perc_25": -0.472607219792436,
                                "median": 0.48539040112024,
                                "perc_75": 1.4080147426271812,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -5.924351030623907,
                            -4.742362244883961,
                            -3.560373459144016,
                            -2.378384673404071,
                            -1.1963958876641252,
                            -0.0144071019241796,
                            1.167581683815765,
                            2.3495704695557116,
                            3.5315592552956563,
                            4.713548041035601,
                            5.895536826775548,
                        ],
                        "reference_values": [
                            24,
                            196,
                            1042,
                            3653,
                            7577,
                            9210,
                            5820,
                            1854,
                            307,
                            28,
                        ],
                    },
                },
                {
                    "feature_name": "feature_4",
                    "type": "numerical",
                    "missing_value": {"count": 301, "percentage": 1.0033333333333334},
                    "mean": -0.0003327321809717066,
                    "std": 1.460907589061218,
                    "min": -7.206236285131561,
                    "max": 6.058136626570091,
                    "median_metrics": {
                        "perc_25": -0.9531061902461275,
                        "median": 0.023245141575466,
                        "perc_75": 0.9741310364527399,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": -0.0027012858089993127,
                            "median_metrics": {
                                "perc_25": -0.8758225222296009,
                                "median": 0.0104414094062951,
                                "perc_75": 0.8858619248113037,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.0020191325374502357,
                            "median_metrics": {
                                "perc_25": -1.0350020658795662,
                                "median": 0.038214277140569755,
                                "perc_75": 1.0792731014939454,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -7.206236285131561,
                            -5.879798993961396,
                            -4.55336170279123,
                            -3.226924411621065,
                            -1.9004871204509,
                            -0.5740498292807343,
                            0.7523874618894304,
                            2.078824753059595,
                            3.4052620442297608,
                            4.731699335399926,
                            6.058136626570091,
                        ],
                        "reference_values": [
                            4,
                            45,
                            465,
                            2360,
                            7180,
                            10590,
                            6885,
                            1899,
                            254,
                            17,
                        ],
                    },
                },
                {
                    "feature_name": "feature_5",
                    "type": "numerical",
                    "missing_value": {"count": 288, "percentage": 0.96},
                    "mean": 0.19382994611338028,
                    "std": 2.2376289283696678,
                    "min": -9.685197606981257,
                    "max": 9.790324559830418,
                    "median_metrics": {
                        "perc_25": -1.1763067000805298,
                        "median": 0.0198519555113513,
                        "perc_75": 1.465839157860066,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.35597196863210107,
                            "median_metrics": {
                                "perc_25": -1.21490084306915,
                                "median": 0.2628897148953393,
                                "perc_75": 1.9052565947885016,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.03262383969215642,
                            "median_metrics": {
                                "perc_25": -1.1462183030748432,
                                "median": -0.1455088310308811,
                                "perc_75": 1.0294832187632506,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -9.685197606981257,
                            -7.73764539030009,
                            -5.790093173618922,
                            -3.8425409569377535,
                            -1.8949887402565864,
                            0.05256347642458081,
                            2.0001156931057498,
                            3.947667909786917,
                            5.895220126468084,
                            7.842772343149251,
                            9.790324559830418,
                        ],
                        "reference_values": [
                            17,
                            148,
                            785,
                            3407,
                            10730,
                            8912,
                            3989,
                            1367,
                            312,
                            45,
                        ],
                    },
                },
                {
                    "feature_name": "feature_6",
                    "type": "numerical",
                    "missing_value": {"count": 307, "percentage": 1.0233333333333334},
                    "mean": -0.12994621965740427,
                    "std": 1.9923923794618597,
                    "min": -10.54458618033603,
                    "max": 11.323501089746786,
                    "median_metrics": {
                        "perc_25": -1.381936111189342,
                        "median": -0.1793887792969184,
                        "perc_75": 1.0459150801924464,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.3261095787594541,
                            "median_metrics": {
                                "perc_25": -1.078578356310297,
                                "median": 0.2967263131302018,
                                "perc_75": 1.686088633372469,
                            },
                        },
                        {
                            "name": "false",
                            "mean": -0.583276279973457,
                            "median_metrics": {
                                "perc_25": -1.5886755026791928,
                                "median": -0.5282321896375355,
                                "perc_75": 0.48473962149726035,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -10.54458618033603,
                            -8.357777453327747,
                            -6.170968726319466,
                            -3.984159999311185,
                            -1.7973512723029028,
                            0.3894574547053793,
                            2.5762661817136596,
                            4.763074908721942,
                            6.949883635730224,
                            9.136692362738504,
                            11.323501089746786,
                        ],
                        "reference_values": [
                            6,
                            57,
                            670,
                            4697,
                            13122,
                            8732,
                            1946,
                            396,
                            63,
                            4,
                        ],
                    },
                },
                {
                    "feature_name": "feature_7",
                    "type": "numerical",
                    "missing_value": {"count": 282, "percentage": 0.9400000000000001},
                    "mean": 0.24162353282697765,
                    "std": 1.553700649763371,
                    "min": -7.2401664809750415,
                    "max": 7.180946563487211,
                    "median_metrics": {
                        "perc_25": -0.7350813046717275,
                        "median": 0.2797318101957035,
                        "perc_75": 1.2432583676125146,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.4616973342907079,
                            "median_metrics": {
                                "perc_25": -0.343341989707933,
                                "median": 0.4743428247688509,
                                "perc_75": 1.288417888040836,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.02267248150832651,
                            "median_metrics": {
                                "perc_25": -1.161954631974072,
                                "median": 0.002494892146202,
                                "perc_75": 1.1827650681915984,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -7.2401664809750415,
                            -5.798055176528816,
                            -4.355943872082591,
                            -2.9138325676363657,
                            -1.4717212631901404,
                            -0.029609958743915143,
                            1.4125013457023101,
                            2.8546126501485354,
                            4.296723954594761,
                            5.738835259040986,
                            7.180946563487211,
                        ],
                        "reference_values": [
                            6,
                            84,
                            654,
                            3163,
                            8449,
                            10996,
                            5098,
                            1083,
                            166,
                            19,
                        ],
                    },
                },
                {
                    "feature_name": "feature_8",
                    "type": "numerical",
                    "missing_value": {"count": 323, "percentage": 1.0766666666666667},
                    "mean": 0.24107080110218446,
                    "std": 1.4328469731071758,
                    "min": -5.145797272829497,
                    "max": 6.12533836079551,
                    "median_metrics": {
                        "perc_25": -0.7079702812609976,
                        "median": 0.2606943392896966,
                        "perc_75": 1.1974171806547638,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": 0.014474852690462928,
                            "median_metrics": {
                                "perc_25": -0.894162877240325,
                                "median": 0.05257934748887095,
                                "perc_75": 0.9632301387950736,
                            },
                        },
                        {
                            "name": "false",
                            "mean": 0.466858839304298,
                            "median_metrics": {
                                "perc_25": -0.4961025561758645,
                                "median": 0.4678176213548028,
                                "perc_75": 1.4327302967981432,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -5.145797272829497,
                            -4.0186837094669965,
                            -2.8915701461044954,
                            -1.7644565827419947,
                            -0.637343019379494,
                            0.4897705439830071,
                            1.6168841073455074,
                            2.7439976707080076,
                            3.8711112340705087,
                            4.99822479743301,
                            6.12533836079551,
                        ],
                        "reference_values": [
                            56,
                            429,
                            1917,
                            5475,
                            8956,
                            7914,
                            3778,
                            975,
                            146,
                            31,
                        ],
                    },
                },
                {
                    "feature_name": "feature_9",
                    "type": "numerical",
                    "missing_value": {"count": 292, "percentage": 0.9733333333333334},
                    "mean": -0.2566905345792553,
                    "std": 1.37062093832564,
                    "min": -5.78428806755016,
                    "max": 5.679876752235,
                    "median_metrics": {
                        "perc_25": -1.1815015799989832,
                        "median": -0.2532013764602815,
                        "perc_75": 0.663191189879565,
                    },
                    "class_median_metrics": [
                        {
                            "name": "true",
                            "mean": -0.03602596321634762,
                            "median_metrics": {
                                "perc_25": -0.960645570131309,
                                "median": -0.0357984468042197,
                                "perc_75": 0.8996846124337728,
                            },
                        },
                        {
                            "name": "false",
                            "mean": -0.4761698524367894,
                            "median_metrics": {
                                "perc_25": -1.3722248160166095,
                                "median": -0.45983661653906327,
                                "perc_75": 0.41867472560944435,
                            },
                        },
                    ],
                    "histogram": {
                        "buckets": [
                            -5.78428806755016,
                            -4.637871585571644,
                            -3.491455103593128,
                            -2.345038621614612,
                            -1.1986221396360959,
                            -0.052205657657579785,
                            1.0942108243209363,
                            2.2406273062994524,
                            3.3870437882779685,
                            4.533460270256485,
                            5.679876752235,
                        ],
                        "reference_values": [
                            24,
                            251,
                            1603,
                            5448,
                            9309,
                            8260,
                            3807,
                            884,
                            111,
                            11,
                        ],
                    },
                },
                {
                    "feature_name": "cat_1",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "c", "count": 10144, "frequency": 0.33813333333333334},
                        {"name": "b", "count": 9908, "frequency": 0.33026666666666665},
                        {"name": "a", "count": 9948, "frequency": 0.3316},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat_2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "f", "count": 9952, "frequency": 0.3317333333333333},
                        {"name": "e", "count": 10122, "frequency": 0.3374},
                        {"name": "d", "count": 9926, "frequency": 0.33086666666666664},
                    ],
                    "distinct_value": 3,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_bool_missing(spark_fixture, dataset_bool_missing):
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
        ColumnDefinition(name="bool1", type=SupportedTypes.bool),
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

    reference_dataset = apply_schema_to_dataframe(
        dataset_bool_missing, model.to_reference_spark_schema()
    )
    reference_dataset = reference_dataset.select(
        *[
            c
            for c in model.to_reference_spark_schema().names
            if c in reference_dataset.columns
        ]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    stats = metrics_service.calculate_statistics()
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats == my_approx(
        {
            "missing_cells": 5,
            "missing_cells_perc": 6.25,
            "duplicate_rows": 2,
            "duplicate_rows_perc": 20.0,
            "n_variables": 8,
            "n_observations": 10,
            "numeric": 5,
            "categorical": 2,
            "datetime": 1,
        }
    )
    assert model_quality == my_approx(
        {
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
                            "mean": 303.56666666666666,
                            "median_metrics": {
                                "perc_25": 142.25,
                                "median": 349.5,
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
                    "feature_name": "bool1",
                    "type": "categorical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "category_frequency": [
                        {"name": "true", "count": 8, "frequency": 0.8},
                        {"name": "false", "count": 1, "frequency": 0.1},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )
