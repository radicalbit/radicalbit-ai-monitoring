import datetime
import uuid
import pytest

from metrics.statistics import calculate_statistics_current
from models.current_dataset import CurrentDataset
from utils.models import (
    ColumnDefinition,
    DataType,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)


@pytest.fixture()
def reference_bike(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/current/regression/bike.csv", header=True
    )


@pytest.fixture()
def current_dataset(reference_bike):
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

    yield CurrentDataset(
        raw_dataframe=reference_bike,
        model=model,
    )


def test_current_statistics(current_dataset):
    stats = calculate_statistics_current(current_dataset)

    assert current_dataset.current_count == stats.n_observations

    assert stats.missing_cells_perc == 100 * stats.missing_cells / (
        stats.n_variables * stats.n_observations
    )

    expected = {
        "n_variables": 14,
        "n_observations": 100,
        "missing_cells": 7,
        "missing_cells_perc": 0.5,
        "duplicate_rows": 2,
        "duplicate_rows_perc": 2.0,
        "numeric": 13,
        "categorical": 0,
        "datetime": 1,
    }

    assert stats.model_dump(serialize_as_any=True) == expected
