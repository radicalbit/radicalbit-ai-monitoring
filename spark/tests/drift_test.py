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

test_resource_path = Path(__file__).resolve().parent / "resources"


@pytest.fixture()
def spark_fixture():
    spark = SparkSession.builder.appName("Drift PyTest").getOrCreate()
    yield spark


@pytest.fixture()
def drift_dataset(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/drift_dataset.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


@pytest.fixture()
def drift_small_dataset(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/drift_small_dataset.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


@pytest.fixture()
def drift_dataset_bool(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/dataset_bool_missing.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset_bool_missing.csv", header=True
        ),
    )


@pytest.fixture()
def drift_dataset_bigger_file(spark_fixture):
    yield (
        spark_fixture.read.csv(
            f"{test_resource_path}/current/drift_dataset_bigger_file.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_resource_path}/reference/dataset.csv", header=True
        ),
    )


def test_drift(spark_fixture, drift_dataset):
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

    current_dataset, reference_dataset = drift_dataset
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

    drift = metrics_service.calculate_drift()

    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.0004993992273872871,
                        "has_drift": False,
                    },
                },
                {
                    "feature_name": "cat2",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.49015296041582523,
                        "has_drift": True,
                    },
                },
                {
                    "feature_name": "num1",
                    "drift_calc": {"type": "KS", "value": 0.9, "has_drift": True},
                },
                {
                    "feature_name": "num2",
                    "drift_calc": {"type": "KS", "value": 0.3, "has_drift": False},
                },
            ]
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_small(spark_fixture, drift_small_dataset):
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

    current_dataset, reference_dataset = drift_small_dataset
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

    drift = metrics_service.calculate_drift()
    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {"type": "CHI2", "value": None, "has_drift": False},
                },
                {
                    "feature_name": "cat2",
                    "drift_calc": {"type": "CHI2", "value": None, "has_drift": False},
                },
                {
                    "feature_name": "num1",
                    "drift_calc": {"type": "KS", "value": 0.75, "has_drift": False},
                },
                {
                    "feature_name": "num2",
                    "drift_calc": {"type": "KS", "value": 0.7, "has_drift": False},
                },
            ]
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_boolean(spark_fixture, drift_dataset_bool):
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

    current_dataset, reference_dataset = drift_dataset_bool
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

    drift = metrics_service.calculate_drift()

    print(drift)

    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.0012340980408668267,
                        "has_drift": False,
                    },
                },
                {
                    "feature_name": "bool1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.002699796063260207,
                        "has_drift": False,
                    },
                },
                {
                    "feature_name": "num1",
                    "drift_calc": {"type": "KS", "value": 0.4, "has_drift": False},
                },
                {
                    "feature_name": "num2",
                    "drift_calc": {"type": "KS", "value": 0.3, "has_drift": False},
                },
            ]
        },
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_bigger_file(spark_fixture, drift_dataset_bigger_file):
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

    current_dataset, reference_dataset = drift_dataset_bigger_file
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

    drift = metrics_service.calculate_drift()

    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.26994857272252293,
                        "has_drift": True,
                    },
                },
                {
                    "feature_name": "cat2",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.3894236957350261,
                        "has_drift": True,
                    },
                },
                {
                    "feature_name": "num1",
                    "drift_calc": {
                        "type": "KS",
                        "value": 0.9230769231,
                        "has_drift": True,
                    },
                },
                {
                    "feature_name": "num2",
                    "drift_calc": {
                        "type": "KS",
                        "value": 0.5384615385,
                        "has_drift": False,
                    },
                },
            ]
        },
        ignore_order=True,
        significant_digits=6,
    )
