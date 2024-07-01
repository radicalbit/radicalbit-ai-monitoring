import datetime
import uuid

import pytest

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


def test_model_quality_metrics(spark_fixture, reference_dataset):
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


def test_statistics_metrics(spark_fixture, reference_dataset):
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
