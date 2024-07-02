import datetime
import uuid

import pytest
import deepdiff

from jobs.metrics.statistics import calculate_statistics_reference
from jobs.utils.reference_regression import ReferenceMetricsRegressionService
from jobs.models.reference_dataset import ReferenceDataset
from jobs.utils.models import (
    ModelOut,
    ModelType,
    DataType,
    OutputType,
    ColumnDefinition,
    SupportedTypes,
    Granularity,
)
from tests.utils.pytest_utils import my_approx


@pytest.fixture()
def reference_bike(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/reference_bike.csv", header=True
    )


@pytest.fixture()
def reference_bike_nulls(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/reference_bike_nulls.csv", header=True
    )


@pytest.fixture()
def expected_data_quality_json():
    yield {
        "n_observations": 731,
        "target_metrics": {
            "feature_name": "ground_truth",
            "type": "numerical",
            "missing_value": {"count": 0, "percentage": 0.0},
            "mean": 848.1764705882352,
            "std": 686.6224882846551,
            "min": 2.0,
            "max": 3410.0,
            "median_metrics": {"perc_25": 315.0, "median": 713.0, "perc_75": 1097.0},
            "histogram": {
                "buckets": [
                    2.0,
                    342.8,
                    683.6,
                    1024.4,
                    1365.2,
                    1706.0,
                    2046.8000000000002,
                    2387.6,
                    2728.4,
                    3069.2000000000003,
                    3410,
                ],
                "reference_values": [
                    204.0,
                    144.0,
                    165.0,
                    89.0,
                    44.0,
                    23.0,
                    26.0,
                    22.0,
                    9.0,
                    5.0,
                ],
            },
        },
        "feature_metrics": [
            {
                "feature_name": "season",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 2.496580027359781,
                "std": 1.1108070927726252,
                "min": 1.0,
                "max": 4.0,
                "median_metrics": {"perc_25": 2.0, "median": 3.0, "perc_75": 3.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        1,
                        1.3,
                        1.6,
                        1.9,
                        2.2,
                        2.5,
                        2.8,
                        3.1,
                        3.4,
                        3.6999999999999997,
                        4,
                    ],
                    "reference_values": [181, 0, 0, 184, 0, 0, 188, 0, 0, 178],
                },
            },
            {
                "feature_name": "yr",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.5006839945280438,
                "std": 0.5003418803818265,
                "min": 0.0,
                "max": 1.0,
                "median_metrics": {"perc_25": 0.0, "median": 1.0, "perc_75": 1.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0,
                        0.1,
                        0.2,
                        0.30000000000000004,
                        0.4,
                        0.5,
                        0.6000000000000001,
                        0.7000000000000001,
                        0.8,
                        0.9,
                        1,
                    ],
                    "reference_values": [365, 0, 0, 0, 0, 0, 0, 0, 0, 366],
                },
            },
            {
                "feature_name": "mnth",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 6.519835841313269,
                "std": 3.451912787256252,
                "min": 1.0,
                "max": 12.0,
                "median_metrics": {"perc_25": 4.0, "median": 7.0, "perc_75": 10.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        1,
                        2.1,
                        3.2,
                        4.300000000000001,
                        5.4,
                        6.5,
                        7.6000000000000005,
                        8.700000000000001,
                        9.8,
                        10.9,
                        12,
                    ],
                    "reference_values": [119, 62, 60, 62, 60, 62, 62, 60, 62, 122],
                },
            },
            {
                "feature_name": "holiday",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.028727770177838577,
                "std": 0.16715474262247393,
                "min": 0.0,
                "max": 1.0,
                "median_metrics": {"perc_25": 0.0, "median": 0.0, "perc_75": 0.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0,
                        0.1,
                        0.2,
                        0.30000000000000004,
                        0.4,
                        0.5,
                        0.6000000000000001,
                        0.7000000000000001,
                        0.8,
                        0.9,
                        1,
                    ],
                    "reference_values": [710, 0, 0, 0, 0, 0, 0, 0, 0, 21],
                },
            },
            {
                "feature_name": "weekday",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 2.997264021887825,
                "std": 2.004786917944481,
                "min": 0.0,
                "max": 6.0,
                "median_metrics": {"perc_25": 1.0, "median": 3.0, "perc_75": 5.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0,
                        0.6,
                        1.2,
                        1.7999999999999998,
                        2.4,
                        3,
                        3.5999999999999996,
                        4.2,
                        4.8,
                        5.3999999999999995,
                        6,
                    ],
                    "reference_values": [105, 105, 0, 104, 0, 104, 104, 0, 104, 105],
                },
            },
            {
                "feature_name": "workingday",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.6839945280437757,
                "std": 0.4652333866777039,
                "min": 0.0,
                "max": 1.0,
                "median_metrics": {"perc_25": 0.0, "median": 1.0, "perc_75": 1.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0,
                        0.1,
                        0.2,
                        0.30000000000000004,
                        0.4,
                        0.5,
                        0.6000000000000001,
                        0.7000000000000001,
                        0.8,
                        0.9,
                        1,
                    ],
                    "reference_values": [231, 0, 0, 0, 0, 0, 0, 0, 0, 500],
                },
            },
            {
                "feature_name": "weathersit",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 1.3953488372093024,
                "std": 0.5448943419593665,
                "min": 1.0,
                "max": 3.0,
                "median_metrics": {"perc_25": 1.0, "median": 1.0, "perc_75": 2.0},
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        1,
                        1.2,
                        1.4,
                        1.6,
                        1.8,
                        2,
                        2.2,
                        2.4000000000000004,
                        2.6,
                        2.8,
                        3,
                    ],
                    "reference_values": [463, 0, 0, 0, 0, 247, 0, 0, 0, 21],
                },
            },
            {
                "feature_name": "temp",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.49538478850889184,
                "std": 0.18305099611148876,
                "min": 0.0591304,
                "max": 0.861667,
                "median_metrics": {
                    "perc_25": 0.3370835,
                    "median": 0.498333,
                    "perc_75": 0.6554165000000001,
                },
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0.0591304,
                        0.13938405999999998,
                        0.21963771999999998,
                        0.29989137999999993,
                        0.38014503999999993,
                        0.46039869999999994,
                        0.5406523599999999,
                        0.62090602,
                        0.70115968,
                        0.78141334,
                        0.861667,
                    ],
                    "reference_values": [7, 36, 90, 104, 93, 80, 93, 101, 103, 24],
                },
            },
            {
                "feature_name": "atemp",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.47435398864569067,
                "std": 0.1629611783863112,
                "min": 0.0790696,
                "max": 0.840896,
                "median_metrics": {
                    "perc_25": 0.3378425,
                    "median": 0.486733,
                    "perc_75": 0.6086020000000001,
                },
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0.0790696,
                        0.15525223999999999,
                        0.23143488,
                        0.30761752,
                        0.38380016,
                        0.45998279999999997,
                        0.53616544,
                        0.61234808,
                        0.6885307199999999,
                        0.7647133599999999,
                        0.840896,
                    ],
                    "reference_values": [11, 34, 97, 99, 98, 93, 122, 112, 57, 8],
                },
            },
            {
                "feature_name": "hum",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.6278940629274962,
                "std": 0.142429095138354,
                "min": 0.0,
                "max": 0.9725,
                "median_metrics": {
                    "perc_25": 0.52,
                    "median": 0.626667,
                    "perc_75": 0.7302085,
                },
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0,
                        0.09725,
                        0.1945,
                        0.29175,
                        0.389,
                        0.48625,
                        0.5835,
                        0.68075,
                        0.778,
                        0.8752500000000001,
                        0.9725,
                    ],
                    "reference_values": [1, 1, 3, 18, 95, 173, 164, 169, 73, 34],
                },
            },
            {
                "feature_name": "windspeed",
                "type": "numerical",
                "missing_value": {"count": 0, "percentage": 0.0},
                "mean": 0.1904862116279068,
                "std": 0.07749787068166944,
                "min": 0.0223917,
                "max": 0.507463,
                "median_metrics": {
                    "perc_25": 0.13495,
                    "median": 0.180975,
                    "perc_75": 0.2332145,
                },
                "class_median_metrics": [],
                "histogram": {
                    "buckets": [
                        0.0223917,
                        0.07089883,
                        0.11940595999999999,
                        0.16791309,
                        0.21642022,
                        0.26492735,
                        0.31343447999999996,
                        0.36194160999999997,
                        0.41044874,
                        0.45895587,
                        0.507463,
                    ],
                    "reference_values": [26, 99, 191, 173, 124, 62, 35, 14, 6, 1],
                },
            },
        ],
    }


@pytest.fixture()
def reference_dataset(spark_fixture, reference_bike):
    output = OutputType(
        prediction=ColumnDefinition(name="predictions", type=SupportedTypes.float),
        prediction_proba=None,
        output=[ColumnDefinition(name="predictions", type=SupportedTypes.float)],
    )
    target = ColumnDefinition(name="ground_truth", type=SupportedTypes.int)
    timestamp = ColumnDefinition(name="dteday", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="season", type=SupportedTypes.int),
        ColumnDefinition(name="yr", type=SupportedTypes.int),
        ColumnDefinition(name="mnth", type=SupportedTypes.int),
        ColumnDefinition(name="holiday", type=SupportedTypes.int),
        ColumnDefinition(name="weekday", type=SupportedTypes.int),
        ColumnDefinition(name="workingday", type=SupportedTypes.int),
        ColumnDefinition(name="weathersit", type=SupportedTypes.float),
        ColumnDefinition(name="temp", type=SupportedTypes.float),
        ColumnDefinition(name="atemp", type=SupportedTypes.float),
        ColumnDefinition(name="hum", type=SupportedTypes.float),
        ColumnDefinition(name="windspeed", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="regression model",
        description="description",
        model_type=ModelType.REGRESSION,
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

    yield ReferenceDataset(
        raw_dataframe=reference_bike,
        model=model,
    )


@pytest.fixture()
def reference_dataset_nulls(spark_fixture, reference_bike_nulls):
    output = OutputType(
        prediction=ColumnDefinition(name="predictions", type=SupportedTypes.float),
        prediction_proba=None,
        output=[ColumnDefinition(name="predictions", type=SupportedTypes.float)],
    )
    target = ColumnDefinition(name="ground_truth", type=SupportedTypes.int)
    timestamp = ColumnDefinition(name="dteday", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="season", type=SupportedTypes.int),
        ColumnDefinition(name="yr", type=SupportedTypes.int),
        ColumnDefinition(name="mnth", type=SupportedTypes.int),
        ColumnDefinition(name="holiday", type=SupportedTypes.int),
        ColumnDefinition(name="weekday", type=SupportedTypes.int),
        ColumnDefinition(name="workingday", type=SupportedTypes.int),
        ColumnDefinition(name="weathersit", type=SupportedTypes.float),
        ColumnDefinition(name="temp", type=SupportedTypes.float),
        ColumnDefinition(name="atemp", type=SupportedTypes.float),
        ColumnDefinition(name="hum", type=SupportedTypes.float),
        ColumnDefinition(name="windspeed", type=SupportedTypes.float),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="regression model",
        description="description",
        model_type=ModelType.REGRESSION,
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

    yield ReferenceDataset(
        raw_dataframe=reference_bike_nulls,
        model=model,
    )


def test_model_quality_metrics(reference_dataset):
    assert reference_dataset.reference_count == 731

    regression_service = ReferenceMetricsRegressionService(reference=reference_dataset)
    model_quality_metrics = regression_service.calculate_model_quality()

    expected = my_approx(
        {
            "mae": 125.0137756497949,
            "mape": 35.193142372738045,
            "mse": 40897.76059849522,
            "rmse": 202.2319475218869,
            "r2": 0.9131323648676931,
            "adj_r2": 0.9118033746222753,
            "var": 393448.3132709007,
        }
    )

    assert model_quality_metrics.model_dump() == expected


def test_statistics_metrics(reference_dataset):
    stats = calculate_statistics_reference(reference_dataset)
    expected = my_approx(
        {
            "missing_cells": 0,
            "missing_cells_perc": 0.0,
            "duplicate_rows": 0,
            "duplicate_rows_perc": 0.0,
            "n_variables": 14,
            "n_observations": 731,
            "numeric": 13,
            "categorical": 0,
            "datetime": 1,
        }
    )

    assert stats.model_dump(serialize_as_any=True) == expected


def test_data_quality_metrics(reference_dataset, expected_data_quality_json):
    regression_service = ReferenceMetricsRegressionService(reference=reference_dataset)
    data_quality = regression_service.calculate_data_quality()

    features = expected_data_quality_json["feature_metrics"]
    target = expected_data_quality_json["target_metrics"]

    computed = data_quality.model_dump(serialize_as_any=True, exclude_none=True)

    computed_features = computed["feature_metrics"]
    computed_target = computed["target_metrics"]

    assert not deepdiff.DeepDiff(
        computed_features,
        features,
        ignore_order=True,
        ignore_type_subclasses=True,
    )

    assert not deepdiff.DeepDiff(
        computed_target,
        target,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_model_quality_metrics_nulls(reference_dataset_nulls):
    regression_service = ReferenceMetricsRegressionService(
        reference=reference_dataset_nulls
    )
    model_quality_metrics = regression_service.calculate_model_quality()

    expected = my_approx(
        {
            "mae": 125.10728395061736,
            "mape": 35.20983108087226,
            "mse": 40967.56920781895,
            "rmse": 202.40446933755922,
            "r2": 0.9130200184348737,
            "adj_r2": 0.9116855975182538,
            "var": 393588.541292358,
        }
    )

    assert model_quality_metrics.model_dump() == expected
