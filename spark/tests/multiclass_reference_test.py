import datetime
import uuid

import deepdiff
import pytest
from utils.reference_multiclass import ReferenceMetricsMulticlassService

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
import tests.results.multiclass_reference_results as res
from tests.utils.pytest_utils import my_approx, prefix_id


@pytest.fixture
def dataset_target_int(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/multiclass/dataset_target_int.csv',
        header=True,
    )


@pytest.fixture
def dataset_target_string(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/multiclass/dataset_target_string.csv',
        header=True,
    )


@pytest.fixture
def dataset_with_nulls(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/multiclass/dataset_target_string_nulls.csv',
        header=True,
    )


@pytest.fixture
def dataset_perfect_classes(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/multiclass/dataset_perfect_classes.csv',
        header=True,
    )


@pytest.fixture
def dataset_indexing(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/multiclass/dataset_target_int_indexing.csv',
        header=True,
    )


def test_calculation_dataset_target_int(spark_fixture, dataset_target_int):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.int,
                field_type=FieldTypes.numerical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.int, field_type=FieldTypes.numerical
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
        model_type=ModelType.MULTI_CLASS,
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
        model=model, raw_dataframe=dataset_target_int, prefix_id=prefix_id
    )

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    data_quality = multiclass_service.calculate_data_quality()
    model_quality = multiclass_service.calculate_model_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_target_int_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_target_int_dq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_dataset_target_int_mq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_target_string(spark_fixture, dataset_target_string):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.string, field_type=FieldTypes.categorical
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
        model_type=ModelType.MULTI_CLASS,
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
        model=model, raw_dataframe=dataset_target_string, prefix_id=prefix_id
    )

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    data_quality = multiclass_service.calculate_data_quality()
    model_quality = multiclass_service.calculate_model_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_target_string_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_target_string_dq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_dataset_target_string_mq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_perfect_classes(spark_fixture, dataset_perfect_classes):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.string, field_type=FieldTypes.categorical
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
        model_type=ModelType.MULTI_CLASS,
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
        model=model, raw_dataframe=dataset_perfect_classes, prefix_id=prefix_id
    )

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    data_quality = multiclass_service.calculate_data_quality()
    model_quality = multiclass_service.calculate_model_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_perfect_classes_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_perfect_classes_dq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_dataset_perfect_classes_mq_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_with_nulls(spark_fixture, dataset_with_nulls):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.string, field_type=FieldTypes.categorical
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
        model_type=ModelType.MULTI_CLASS,
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

    reference_dataframe = dataset_with_nulls
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_dataframe, prefix_id=prefix_id
    )

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    model_quality = multiclass_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_dataset_with_nulls_res,
        ignore_order=True,
        significant_digits=6,
    )


def test_calculation_dataset_indexing(spark_fixture, dataset_indexing):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.int,
                field_type=FieldTypes.numerical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.int, field_type=FieldTypes.numerical
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
        model_type=ModelType.MULTI_CLASS,
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
        model=model, raw_dataframe=dataset_indexing, prefix_id=prefix_id
    )

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    model_quality = multiclass_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_dataset_indexing_res,
        ignore_order=True,
        significant_digits=6,
    )
