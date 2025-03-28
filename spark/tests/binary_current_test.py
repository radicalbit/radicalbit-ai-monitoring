import datetime
import uuid

import deepdiff
import pytest

from jobs.metrics.statistics import calculate_statistics_current
from jobs.models.current_dataset import CurrentDataset
from jobs.models.reference_dataset import ReferenceDataset
from jobs.utils.current_binary import CurrentMetricsService
from jobs.utils.models import (
    ColumnDefinition,
    DataType,
    FieldTypes,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)
import tests.results.binary_current_results as res
from tests.utils.pytest_utils import my_approx, prefix_id


@pytest.fixture
def dataset(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(f'{test_data_dir}/current/dataset.csv', header=True),
        spark_fixture.read.csv(f'{test_data_dir}/reference/dataset.csv', header=True),
    )


@pytest.fixture
def complete_dataset(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/complete_dataset.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/complete_dataset.csv', header=True
        ),
    )


@pytest.fixture
def current_joined(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/current_joined.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/reference_joined.csv', header=True
        ),
    )


@pytest.fixture
def easy_dataset(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/easy_dataset.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/easy_dataset.csv', header=True
        ),
    )


@pytest.fixture
def dataset_cat_missing(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_cat_missing.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/dataset_cat_missing.csv', header=True
        ),
    )


@pytest.fixture
def dataset_with_datetime(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_with_datetime.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/dataset_with_datetime.csv', header=True
        ),
    )


@pytest.fixture
def easy_dataset_bucket_test(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/easy_dataset_bucket_test.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/easy_dataset.csv', header=True
        ),
    )


@pytest.fixture
def dataset_for_hour(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_for_hour.csv', header=True
        ),
        spark_fixture.read.csv(f'{test_data_dir}/reference/dataset.csv', header=True),
    )


@pytest.fixture
def dataset_for_day(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_for_day.csv', header=True
        ),
        spark_fixture.read.csv(f'{test_data_dir}/reference/dataset.csv', header=True),
    )


@pytest.fixture
def dataset_for_week(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_for_week.csv', header=True
        ),
        spark_fixture.read.csv(f'{test_data_dir}/reference/dataset.csv', header=True),
    )


@pytest.fixture
def dataset_for_month(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_for_month.csv', header=True
        ),
        spark_fixture.read.csv(f'{test_data_dir}/reference/dataset.csv', header=True),
    )


@pytest.fixture
def dataset_with_nulls(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/dataset_nulls.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/dataset_nulls.csv', header=True
        ),
    )


def test_calculation(spark_fixture, dataset):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_stats_res
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_mq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_current_joined(spark_fixture, current_joined):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='age', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='sex', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='chest_pain_type',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='resting_blood_pressure',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='cholesterol', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='fasting_blood_sugar',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='resting_ecg', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='max_heart_rate_achieved',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='exercise_induced_angina',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='st_depression',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='st_slope', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = current_joined
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_current_joined_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_current_joined_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_complete(spark_fixture, complete_dataset):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.bool, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = complete_dataset
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_complete_stats_res,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_complete_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_easy_dataset(spark_fixture, easy_dataset):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = easy_dataset
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_easy_dataset_stats_res,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_easy_dataset_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_cat_missing(spark_fixture, dataset_cat_missing):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_cat_missing
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_cat_missing_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_cat_missing_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_with_datetime(spark_fixture, dataset_with_datetime):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_with_datetime
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_with_datetime_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_with_datetime_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_easy_dataset_bucket_test(spark_fixture, easy_dataset_bucket_test):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = easy_dataset_bucket_test
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_easy_dataset_bucket_test_stats_res,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_easy_dataset_bucket_test_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_hour(spark_fixture, dataset_for_hour):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_for_hour
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_for_hour_stats_res
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_for_hour_mq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_for_hour_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_day(spark_fixture, dataset_for_day):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.DAY
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_for_day
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_for_day_stats_res
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_for_day_mq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_for_day_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_week(spark_fixture, dataset_for_week):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.WEEK
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_for_week
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_for_week_stats_res
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_for_week_mq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_for_week_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_for_month(spark_fixture, dataset_for_month):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_for_month
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    stats = calculate_statistics_current(current_dataset)
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_for_month_stats_res
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_for_month_mq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_for_month_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_model_quality_nulls(spark_fixture, dataset_with_nulls):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(
            name='cat1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat2', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='num1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='num2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = dataset_with_nulls
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_model_quality_nulls_res,
        ignore_order=True,
        significant_digits=6,
    )
