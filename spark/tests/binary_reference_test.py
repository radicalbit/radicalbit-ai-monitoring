import datetime
import uuid

import deepdiff
import pytest

from jobs.metrics.statistics import calculate_statistics_reference
from jobs.models.reference_dataset import ReferenceDataset
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
from jobs.utils.reference_binary import ReferenceMetricsService
import tests.results.binary_reference_results as res
from tests.utils.pytest_utils import my_approx, prefix_id


@pytest.fixture
def dataset(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(f'{test_data_dir}/reference/dataset.csv', header=True)


@pytest.fixture
def complete_dataset(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/complete_dataset.csv', header=True
    )


@pytest.fixture
def reference_joined(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/reference_joined.csv', header=True
    )


@pytest.fixture
def easy_dataset(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/easy_dataset.csv', header=True
    )


@pytest.fixture
def dataset_cat_missing(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/dataset_cat_missing.csv', header=True
    )


@pytest.fixture
def dataset_with_datetime(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/dataset_with_datetime.csv', header=True
    )


@pytest.fixture
def enhanced_data(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/enhanced_data.csv', header=True
    )


@pytest.fixture
def dataset_bool_missing(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/dataset_bool_missing.csv', header=True
    )


@pytest.fixture
def dataset_with_nulls(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/dataset_nulls.csv', header=True
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=dataset, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_stats_res
    )
    assert model_quality == my_approx(res.test_calculation_mq_res)

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_reference_joined(spark_fixture, reference_joined):
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_joined, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_reference_joined_stats_res
    )
    assert model_quality == my_approx(
        res.test_calculation_reference_joined_mq_res,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_reference_joined_dq_res,
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=complete_dataset, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_complete_stats_res,
    )

    assert model_quality == my_approx(
        res.test_calculation_complete_mq_res,
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=easy_dataset, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_easy_dataset_stats_res,
    )
    assert model_quality == my_approx(
        res.test_calculation_easy_dataset_mq_res,
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=dataset_cat_missing, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_cat_missing_stats_res
    )
    assert model_quality == my_approx(
        res.test_calculation_dataset_cat_missing_mq_res,
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=dataset_with_datetime, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_with_datetime_stats_res
    )
    assert model_quality == my_approx(res.test_calculation_dataset_with_datetime_mq_res)

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_with_datetime_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_enhanced_data(spark_fixture, enhanced_data):
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
            name='feature_0', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_1', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_2', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_3', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_4', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_5', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_6', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_7', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_8', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='feature_9', type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name='cat_1', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='cat_2', type=SupportedTypes.string, field_type=FieldTypes.categorical
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=enhanced_data, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_enhanced_data_stats_res
    )
    assert model_quality == my_approx(res.test_calculation_enhanced_data_mq_res)

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_enhanced_data_dq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_bool_missing(spark_fixture, dataset_bool_missing):
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
            name='bool1', type=SupportedTypes.bool, field_type=FieldTypes.categorical
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=dataset_bool_missing, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    model_quality = metrics_service.calculate_model_quality()
    data_quality = metrics_service.calculate_data_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_bool_missing_stats_res
    )
    assert model_quality == my_approx(
        res.test_calculation_dataset_bool_missing_mq_res,
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_bool_missing_dq_res,
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

    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=dataset_with_nulls, prefix_id=prefix_id
    )
    metrics_service = ReferenceMetricsService(reference_dataset, prefix_id)

    model_quality = metrics_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_model_quality_nulls_res,
        ignore_order=True,
        significant_digits=6,
    )
