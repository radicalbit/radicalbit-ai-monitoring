import datetime
import uuid
from pathlib import Path

import pytest
from pyspark.sql import SparkSession

from jobs.metrics.statistics import calculate_statistics_reference
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

test_resource_path = Path(__file__).resolve().parent / "resources"


@pytest.fixture()
def spark_fixture():
    spark = SparkSession.builder.appName("Reference Multiclass PyTest").getOrCreate()
    yield spark


@pytest.fixture()
def dataset_target_int(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/multiclass/dataset_target_int.csv", header=True
    )


@pytest.fixture()
def dataset_target_string(spark_fixture):
    yield spark_fixture.read.csv(
        f"{test_resource_path}/reference/multiclass/dataset_target_string.csv",
        header=True,
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

    reference_dataset = ReferenceDataset(model=model, raw_dataframe=dataset_target_int)

    stats = calculate_statistics_reference(reference_dataset)

    assert stats == my_approx(
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=dataset_target_string
    )

    stats = calculate_statistics_reference(reference_dataset)

    assert stats == my_approx(
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
