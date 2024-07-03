import datetime
import uuid

import deepdiff
import pytest

from jobs.models.current_dataset import CurrentDataset
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
from metrics.drift_calculator import DriftCalculator


@pytest.fixture()
def drift_dataset(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/drift_dataset.csv", header=True
        ),
        spark_fixture.read.csv(f"{test_data_dir}/reference/dataset.csv", header=True),
    )


@pytest.fixture()
def drift_small_dataset(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/drift_small_dataset.csv", header=True
        ),
        spark_fixture.read.csv(f"{test_data_dir}/reference/dataset.csv", header=True),
    )


@pytest.fixture()
def drift_dataset_bool(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/dataset_bool_missing.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/dataset_bool_missing.csv", header=True
        ),
    )


@pytest.fixture()
def drift_dataset_bigger_file(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/drift_dataset_bigger_file.csv", header=True
        ),
        spark_fixture.read.csv(f"{test_data_dir}/reference/dataset.csv", header=True),
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

    raw_current_dataset, raw_reference_dataset = drift_dataset
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset
    )

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
    )

    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.0004993992273872871,
                        "has_drift": True,
                    },
                },
                {
                    "feature_name": "cat2",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.49015296041582523,
                        "has_drift": False,
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

    raw_current_dataset, raw_reference_dataset = drift_small_dataset
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
    )

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

    raw_current_dataset, raw_reference_dataset = drift_dataset_bool
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
    )

    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.0012340980408668267,
                        "has_drift": True,
                    },
                },
                {
                    "feature_name": "bool1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.002699796063260207,
                        "has_drift": True,
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

    raw_current_dataset, raw_reference_dataset = drift_dataset_bigger_file
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
    )

    assert not deepdiff.DeepDiff(
        drift,
        {
            "feature_metrics": [
                {
                    "feature_name": "cat1",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.26994857272252293,
                        "has_drift": False,
                    },
                },
                {
                    "feature_name": "cat2",
                    "drift_calc": {
                        "type": "CHI2",
                        "value": 0.3894236957350261,
                        "has_drift": False,
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
