import datetime
import uuid

import deepdiff
import pytest

from jobs.metrics.statistics import calculate_statistics_current
from jobs.utils.models import (
    ModelOut,
    ModelType,
    DataType,
    OutputType,
    ColumnDefinition,
    SupportedTypes,
    Granularity,
)
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from tests.utils.pytest_utils import my_approx
from utils.current_multiclass import CurrentMetricsMulticlassService


@pytest.fixture()
def dataset_target_int(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/multiclass/dataset_target_int.csv",
            header=True,
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/current/multiclass/dataset_target_int.csv",
            header=True,
        ),
    )


@pytest.fixture()
def dataset_target_string(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/multiclass/dataset_target_string.csv",
            header=True,
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/current/multiclass/dataset_target_string.csv",
            header=True,
        ),
    )


@pytest.fixture()
def dataset_with_nulls(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/multiclass/dataset_target_string_nulls.csv",
            header=True,
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/current/multiclass/dataset_target_string_nulls.csv",
            header=True,
        ),
    )


@pytest.fixture()
def dataset_perfect_classes(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/multiclass/dataset_perfect_classes.csv",
            header=True,
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/current/multiclass/dataset_perfect_classes.csv",
            header=True,
        ),
    )


@pytest.fixture()
def dataset_for_hour(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/multiclass/dataset_for_hour.csv",
            header=True,
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/current/multiclass/dataset_for_hour.csv",
            header=True,
        ),
    )


def test_calculation_dataset_target_int(spark_fixture, dataset_target_int):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.int),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.int)],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.int)
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
        model_type=ModelType.MULTI_CLASS,
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

    current_dataframe, reference_dataframe = dataset_target_int
    current_dataset = CurrentDataset(model=model, raw_dataframe=current_dataframe)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=reference_dataframe)

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality()

    stats = calculate_statistics_current(current_dataset)

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        {
            "categorical": 2,
            "datetime": 1,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
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
                {"name": "0", "count": 3, "percentage": 30.0},
                {"name": "1", "count": 3, "percentage": 30.0},
                {"name": "2", "count": 3, "percentage": 30.0},
                {"name": "3", "count": 1, "percentage": 10.0},
            ],
            "class_metrics_prediction": [
                {"name": "0", "count": 2, "percentage": 20.0},
                {"name": "1", "count": 4, "percentage": 40.0},
                {"name": "2", "count": 2, "percentage": 20.0},
                {"name": "3", "count": 2, "percentage": 20.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.75,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [],
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
                    "class_median_metrics": [],
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
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                        {"name": "A", "count": 5, "frequency": 0.5},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "Y", "count": 1, "frequency": 0.1},
                        {"name": "X", "count": 9, "frequency": 0.9},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "classes": ["0", "1", "2", "3"],
            "class_metrics": [
                {
                    "class_name": "0",
                    "metrics": {
                        "true_positive_rate": 0.6666666666666666,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 0.6666666666666666,
                        "f_measure": 0.8,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.6666666666666666,
                            }
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.6666666666666666,
                            }
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.8}
                        ],
                    },
                },
                {
                    "class_name": "1",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.14285714285714285,
                        "precision": 0.75,
                        "recall": 1.0,
                        "f_measure": 0.8571428571428571,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.14285714285714285,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.75}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.8571428571428571,
                            }
                        ],
                    },
                },
                {
                    "class_name": "2",
                    "metrics": {
                        "true_positive_rate": 0.3333333333333333,
                        "false_positive_rate": 0.14285714285714285,
                        "precision": 0.5,
                        "recall": 0.3333333333333333,
                        "f_measure": 0.4,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.3333333333333333,
                            }
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.14285714285714285,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.5}
                        ],
                        "recall": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.3333333333333333,
                            }
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.4}
                        ],
                    },
                },
                {
                    "class_name": "3",
                    "metrics": {
                        "true_positive_rate": 0.0,
                        "false_positive_rate": 0.2222222222222222,
                        "precision": 0.0,
                        "recall": 0.0,
                        "f_measure": 0.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.2222222222222222,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 0.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                    },
                },
            ],
            "global_metrics": {
                "f1": 0.6171428571428572,
                "accuracy": 0.6,
                "weighted_precision": 0.675,
                "weighted_recall": 0.6000000000000001,
                "weighted_true_positive_rate": 0.6000000000000001,
                "weighted_false_positive_rate": 0.10793650793650794,
                "weighted_f_measure": 0.6171428571428572,
                "confusion_matrix": [
                    [2.0, 0.0, 1.0, 0.0],
                    [0.0, 3.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 2.0],
                    [0.0, 1.0, 0.0, 0.0],
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_target_string(spark_fixture, dataset_target_string):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.string),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.string)],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.string)
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
        model_type=ModelType.MULTI_CLASS,
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

    current_dataframe, reference_dataframe = dataset_target_string
    current_dataset = CurrentDataset(model=model, raw_dataframe=current_dataframe)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=reference_dataframe)

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality()
    stats = calculate_statistics_current(current_dataset)

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        {
            "categorical": 4,
            "datetime": 1,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 2,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "HEALTHY", "count": 3, "percentage": 30.0},
                {"name": "ORPHAN", "count": 1, "percentage": 10.0},
                {"name": "UNHEALTHY", "count": 3, "percentage": 30.0},
                {"name": "UNKNOWN", "count": 3, "percentage": 30.0},
            ],
            "class_metrics_prediction": [
                {"name": "HEALTHY", "count": 4, "percentage": 40.0},
                {"name": "ORPHAN", "count": 2, "percentage": 20.0},
                {"name": "UNHEALTHY", "count": 2, "percentage": 20.0},
                {"name": "UNKNOWN", "count": 2, "percentage": 20.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.75,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [],
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
                    "class_median_metrics": [],
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
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                        {"name": "A", "count": 5, "frequency": 0.5},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "Y", "count": 1, "frequency": 0.1},
                        {"name": "X", "count": 9, "frequency": 0.9},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "classes": ["HEALTHY", "ORPHAN", "UNHEALTHY", "UNKNOWN"],
            "class_metrics": [
                {
                    "class_name": "HEALTHY",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.14285714285714285,
                        "precision": 0.75,
                        "recall": 1.0,
                        "f_measure": 0.8571428571428571,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.14285714285714285,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.75}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.8571428571428571,
                            }
                        ],
                    },
                },
                {
                    "class_name": "ORPHAN",
                    "metrics": {
                        "true_positive_rate": 0.0,
                        "false_positive_rate": 0.2222222222222222,
                        "precision": 0.0,
                        "recall": 0.0,
                        "f_measure": 0.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.2222222222222222,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 0.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                    },
                },
                {
                    "class_name": "UNHEALTHY",
                    "metrics": {
                        "true_positive_rate": 0.6666666666666666,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 0.6666666666666666,
                        "f_measure": 0.8,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.6666666666666666,
                            }
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.6666666666666666,
                            }
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.8}
                        ],
                    },
                },
                {
                    "class_name": "UNKNOWN",
                    "metrics": {
                        "true_positive_rate": 0.3333333333333333,
                        "false_positive_rate": 0.14285714285714285,
                        "precision": 0.5,
                        "recall": 0.3333333333333333,
                        "f_measure": 0.4,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.3333333333333333,
                            }
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.14285714285714285,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.5}
                        ],
                        "recall": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.3333333333333333,
                            }
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.4}
                        ],
                    },
                },
            ],
            "global_metrics": {
                "f1": 0.6171428571428572,
                "accuracy": 0.6,
                "weighted_precision": 0.6749999999999999,
                "weighted_recall": 0.6000000000000001,
                "weighted_true_positive_rate": 0.6000000000000001,
                "weighted_false_positive_rate": 0.10793650793650793,
                "weighted_f_measure": 0.6171428571428572,
                "confusion_matrix": [
                    [3.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 1.0],
                    [0.0, 2.0, 0.0, 1.0],
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_perfect_classes(spark_fixture, dataset_perfect_classes):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.string),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.string)],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.string)
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
        model_type=ModelType.MULTI_CLASS,
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

    current_dataframe, reference_dataframe = dataset_perfect_classes
    current_dataset = CurrentDataset(model=model, raw_dataframe=current_dataframe)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=reference_dataframe)

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality()
    stats = calculate_statistics_current(current_dataset)

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        {
            "categorical": 4,
            "datetime": 1,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 2,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "HEALTHY", "count": 4, "percentage": 40.0},
                {"name": "ORPHAN", "count": 2, "percentage": 20.0},
                {"name": "UNHEALTHY", "count": 2, "percentage": 20.0},
                {"name": "UNKNOWN", "count": 2, "percentage": 20.0},
            ],
            "class_metrics_prediction": [
                {"name": "HEALTHY", "count": 4, "percentage": 40.0},
                {"name": "ORPHAN", "count": 2, "percentage": 20.0},
                {"name": "UNHEALTHY", "count": 2, "percentage": 20.0},
                {"name": "UNKNOWN", "count": 2, "percentage": 20.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.75,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [],
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
                    "class_median_metrics": [],
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
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                        {"name": "A", "count": 5, "frequency": 0.5},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "Y", "count": 1, "frequency": 0.1},
                        {"name": "X", "count": 9, "frequency": 0.9},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "classes": ["HEALTHY", "ORPHAN", "UNHEALTHY", "UNKNOWN"],
            "class_metrics": [
                {
                    "class_name": "HEALTHY",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 1.0,
                        "f_measure": 1.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                    },
                },
                {
                    "class_name": "ORPHAN",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 1.0,
                        "f_measure": 1.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                    },
                },
                {
                    "class_name": "UNHEALTHY",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 1.0,
                        "f_measure": 1.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                    },
                },
                {
                    "class_name": "UNKNOWN",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 1.0,
                        "f_measure": 1.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                    },
                },
            ],
            "global_metrics": {
                "f1": 1.0,
                "accuracy": 1.0,
                "weighted_precision": 1.0,
                "weighted_recall": 1.0,
                "weighted_true_positive_rate": 1.0,
                "weighted_false_positive_rate": 0.0,
                "weighted_f_measure": 1.0,
                "confusion_matrix": [
                    [4.0, 0.0, 0.0, 0.0],
                    [0.0, 2.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 0.0],
                    [0.0, 0.0, 0.0, 2.0],
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_for_hour(spark_fixture, dataset_for_hour):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.string),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.string)],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.string)
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
        model_type=ModelType.MULTI_CLASS,
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

    current_dataframe, reference_dataframe = dataset_for_hour
    current_dataset = CurrentDataset(model=model, raw_dataframe=current_dataframe)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=reference_dataframe)

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    data_quality = metrics_service.calculate_data_quality()

    model_quality = metrics_service.calculate_model_quality()

    stats = calculate_statistics_current(current_dataset)

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        {
            "categorical": 4,
            "datetime": 1,
            "duplicate_rows": 1,
            "duplicate_rows_perc": 10.0,
            "missing_cells": 3,
            "missing_cells_perc": 4.285714285714286,
            "n_observations": 10,
            "n_variables": 7,
            "numeric": 2,
        }
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        {
            "n_observations": 10,
            "class_metrics": [
                {"name": "CAT", "count": 5, "percentage": 50.0},
                {"name": "COW", "count": 3, "percentage": 30.0},
                {"name": "DOG", "count": 2, "percentage": 20.0},
            ],
            "class_metrics_prediction": [
                {"name": "CAT", "count": 4, "percentage": 40.0},
                {"name": "COW", "count": 3, "percentage": 30.0},
                {"name": "DOG", "count": 3, "percentage": 30.0},
            ],
            "feature_metrics": [
                {
                    "feature_name": "num1",
                    "type": "numerical",
                    "missing_value": {"count": 1, "percentage": 10.0},
                    "mean": 1.1666666666666667,
                    "std": 0.75,
                    "min": 0.5,
                    "max": 3.0,
                    "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 1.0},
                    "class_median_metrics": [],
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
                    "class_median_metrics": [],
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
                        {"name": "B", "count": 4, "frequency": 0.4},
                        {"name": "C", "count": 1, "frequency": 0.1},
                        {"name": "A", "count": 5, "frequency": 0.5},
                    ],
                    "distinct_value": 3,
                },
                {
                    "feature_name": "cat2",
                    "type": "categorical",
                    "missing_value": {"count": 0, "percentage": 0.0},
                    "category_frequency": [
                        {"name": "Y", "count": 1, "frequency": 0.1},
                        {"name": "X", "count": 9, "frequency": 0.9},
                    ],
                    "distinct_value": 2,
                },
            ],
        },
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "classes": ["CAT", "COW", "DOG"],
            "class_metrics": [
                {
                    "class_name": "CAT",
                    "metrics": {
                        "true_positive_rate": 0.6,
                        "false_positive_rate": 0.2,
                        "precision": 0.75,
                        "recall": 0.6,
                        "f_measure": 0.6666666666666665,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                        ],
                        "recall": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": 1.0},
                        ],
                    },
                },
                {
                    "class_name": "COW",
                    "metrics": {
                        "true_positive_rate": 0.6666666666666666,
                        "false_positive_rate": 0.14285714285714285,
                        "precision": 0.6666666666666666,
                        "recall": 0.6666666666666666,
                        "f_measure": 0.6666666666666666,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 01:00:00", "value": 0.5},
                            {"timestamp": "2024-06-16 02:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 03:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 01:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 02:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "recall": [
                            {"timestamp": "2024-06-16 00:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 01:00:00", "value": 0.5},
                            {"timestamp": "2024-06-16 02:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": float("nan")},
                            {
                                "timestamp": "2024-06-16 01:00:00",
                                "value": 0.6666666666666666,
                            },
                            {"timestamp": "2024-06-16 02:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 03:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                    },
                },
                {
                    "class_name": "DOG",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.125,
                        "precision": 0.6666666666666666,
                        "recall": 1.0,
                        "f_measure": 0.8,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.5},
                            {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 0.5},
                            {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "recall": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 02:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0},
                            {"timestamp": "2024-06-16 01:00:00", "value": float("nan")},
                            {
                                "timestamp": "2024-06-16 02:00:00",
                                "value": 0.6666666666666666,
                            },
                            {"timestamp": "2024-06-16 03:00:00", "value": float("nan")},
                            {"timestamp": "2024-06-16 04:00:00", "value": float("nan")},
                        ],
                    },
                },
            ],
            "global_metrics": {
                "f1": 0.6933333333333332,
                "accuracy": 0.7,
                "weighted_precision": 0.7083333333333334,
                "weighted_recall": 0.7,
                "weighted_true_positive_rate": 0.7,
                "weighted_false_positive_rate": 0.16785714285714287,
                "weighted_f_measure": 0.6933333333333332,
                "confusion_matrix": [[3.0, 1.0, 1.0], [1.0, 2.0, 0.0], [0.0, 0.0, 2.0]],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_with_nulls(spark_fixture, dataset_with_nulls):
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.string),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.string)],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.string)
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
        model_type=ModelType.MULTI_CLASS,
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

    current_dataframe, reference_dataframe = dataset_with_nulls
    current_dataset = CurrentDataset(model=model, raw_dataframe=current_dataframe)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=reference_dataframe)

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    model_quality = metrics_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        {
            "classes": ["HEALTHY", "ORPHAN", "UNHEALTHY", "UNKNOWN"],
            "class_metrics": [
                {
                    "class_name": "HEALTHY",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.16666666666666666,
                        "precision": 0.6666666666666666,
                        "recall": 1.0,
                        "f_measure": 0.8,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.16666666666666666,
                            }
                        ],
                        "precision": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.6666666666666666,
                            }
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.8}
                        ],
                    },
                },
                {
                    "class_name": "ORPHAN",
                    "metrics": {
                        "true_positive_rate": 0.0,
                        "false_positive_rate": 0.2857142857142857,
                        "precision": 0.0,
                        "recall": 0.0,
                        "f_measure": 0.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "false_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.2857142857142857,
                            }
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 0.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                    },
                },
                {
                    "class_name": "UNHEALTHY",
                    "metrics": {
                        "true_positive_rate": 1.0,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 1.0,
                        "f_measure": 1.0,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [{"timestamp": "2024-06-16 00:00:00", "value": 1.0}],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                    },
                },
                {
                    "class_name": "UNKNOWN",
                    "metrics": {
                        "true_positive_rate": 0.3333333333333333,
                        "false_positive_rate": 0.0,
                        "precision": 1.0,
                        "recall": 0.3333333333333333,
                        "f_measure": 0.5,
                    },
                    "grouped_metrics": {
                        "true_positive_rate": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.3333333333333333,
                            }
                        ],
                        "false_positive_rate": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.0}
                        ],
                        "precision": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 1.0}
                        ],
                        "recall": [
                            {
                                "timestamp": "2024-06-16 00:00:00",
                                "value": 0.3333333333333333,
                            }
                        ],
                        "f_measure": [
                            {"timestamp": "2024-06-16 00:00:00", "value": 0.5}
                        ],
                    },
                },
            ],
            "global_metrics": {
                "f1": 0.6375,
                "accuracy": 0.625,
                "weighted_precision": 0.7916666666666666,
                "weighted_recall": 0.625,
                "weighted_true_positive_rate": 0.625,
                "weighted_false_positive_rate": 0.07738095238095238,
                "weighted_f_measure": 0.6375,
                "confusion_matrix": [
                    [2.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 2.0, 0.0],
                    [0.0, 2.0, 0.0, 1.0],
                ],
            },
        },
        ignore_order=True,
        significant_digits=6,
    )
