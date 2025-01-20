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
    FieldTypes,
    Granularity,
)
from metrics.drift_calculator import DriftCalculator
import tests.results.drift_calculator_results as res
from tests.utils.pytest_utils import prefix_id

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


@pytest.fixture()
def drift_dataset_bike(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/regression/bike.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/regression/reference_bike.csv", header=True
        ),
    )


@pytest.fixture()
def drift_dataset_phone(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/current_phone_drift_dataset.csv", header=True
        ),
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/reference_phone_drift_dataset.csv", header=True
        ),
    )


def test_drift(spark_fixture, drift_dataset):
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name="prediction_proba",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name="prediction_proba",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="datetime", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="cat1", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="cat2", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="num1", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="num2", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
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
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id
    )

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_small(spark_fixture, drift_small_dataset):
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name="prediction_proba",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name="prediction_proba",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="datetime", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="cat1", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="cat2", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="num1", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="num2", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
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
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id
    )

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_small_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_boolean(spark_fixture, drift_dataset_bool):
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name="prediction_proba",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name="prediction_proba",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="datetime", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="cat1", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="bool1", type=SupportedTypes.bool, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="num1", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="num2", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
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
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id
    )

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_boolean_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_bigger_file(spark_fixture, drift_dataset_bigger_file):
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name="prediction_proba",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name="prediction_proba",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="datetime", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="cat1", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="cat2", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="num1", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="num2", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
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
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id
    )

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_bigger_file_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_bike(spark_fixture, drift_dataset_bike):
    output = OutputType(
        prediction=ColumnDefinition(
            name="predictions",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name="predictions",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            )
        ],
    )
    target = ColumnDefinition(
        name="ground_truth", type=SupportedTypes.int, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="dteday", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="season", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="yr", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="mnth", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="holiday", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="weekday", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="workingday",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="weathersit",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="temp", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="atemp", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="hum", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="windspeed", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
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

    raw_current_dataset, raw_reference_dataset = drift_dataset_bike
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id
    )

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_bike_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_phone(spark_fixture, drift_dataset_phone):
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name="prediction_proba",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name="prediction_proba",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="timestamp", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(
            name="brand_name",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="model", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="price", type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="rating", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="has_5g", type=SupportedTypes.bool, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="has_nfc", type=SupportedTypes.bool, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="has_ir_blaster",
            type=SupportedTypes.bool,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="processor_brand",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="num_cores", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="processor_speed",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="battery_capacity",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="fast_charging_available",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="fast_charging",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="ram_capacity",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="internal_memory",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="screen_size",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="refresh_rate",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="num_rear_cameras",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="num_front_cameras",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="os", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="primary_camera_rear",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="primary_camera_front",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="extended_memory_available",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="extended_upto",
            type=SupportedTypes.float,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="resolution_width",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="resolution_height",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="binary model",
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

    raw_current_dataset, raw_reference_dataset = drift_dataset_phone
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )
    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id
    )

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_phone_res,
        ignore_order=True,
        significant_digits=6,
    )
