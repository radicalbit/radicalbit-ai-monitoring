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
def dataset_perfect_classs(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/multiclass/dataset_perfect_classs.csv',
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


def test_calculation_dataset_perfect_classs(spark_fixture, dataset_perfect_classs):
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
        model=model, raw_dataframe=dataset_perfect_classs, prefix_id=prefix_id
    )

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    stats = calculate_statistics_reference(reference_dataset)
    data_quality = multiclass_service.calculate_data_quality()
    model_quality = multiclass_service.calculate_model_quality()

    assert stats.model_dump(serialize_as_any=True) == my_approx(
        res.test_calculation_dataset_perfect_classs_stats_res
    )

    assert not deepdiff.DeepDiff(
        data_quality.model_dump(serialize_as_any=True, exclude_none=True),
        res.test_calculation_dataset_perfect_classs_dq_res,
        ignore_order=True,
        significant_digits=6,
    )

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_calculation_dataset_perfect_classs_mq_res,
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


def test_categorical_features_mixed_types_fixed(spark_fixture):
    # Create a dataset with categorical features of mixed types
    data = [
        ('A', '123', 'X', 10, 1.5, 2.0, 'cat1', 'desc1', 1, '2023-01-01 10:00:00', 0),
        ('B', '456', 'Y', 20, 2.5, 3.0, 'cat2', 'desc2', 2, '2023-01-01 11:00:00', 1),
        ('C', '789', 'Z', 30, 3.5, 4.0, 'cat3', 'desc3', 0, '2023-01-01 12:00:00', 2),
    ]

    columns = [
        'title',  # STRING - categorical
        'code',  # STRING - categorical
        'sec',  # STRING - categorical
        'dive',  # INT - categorical
        'group',  # DOUBLE - categorical
        'class',  # DOUBLE - categorical
        'category',  # STRING - categorical
        'desc',  # STRING - categorical
        'prediction',  # INT
        'datetime',  # TIMESTAMP
        'target',  # INT
    ]

    dataset = spark_fixture.createDataFrame(data, columns)

    # Define model with ALL features as categorical to trigger the error
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

    # Define all the different-typed columns as categorical features
    # This is what triggers the bug
    features = [
        ColumnDefinition(
            name='title', type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='code',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name='sec',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name='dive', type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='group', type=SupportedTypes.float, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='class', type=SupportedTypes.float, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name='category',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name='desc',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
    ]

    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.MULTI_CLASS,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=Granularity.HOUR,
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

    multiclass_service = ReferenceMetricsMulticlassService(reference_dataset, prefix_id)

    # This should now work with the fix (casting all categorical columns to STRING)
    data_quality = multiclass_service.calculate_data_quality()

    # Verify the data quality was calculated successfully
    assert data_quality is not None
    assert data_quality.n_observations == 3
    assert len(data_quality.feature_metrics) == 8  # All 8 categorical features

    # Verify all features are present with their metrics
    feature_names = {fm.feature_name for fm in data_quality.feature_metrics}
    expected_features = {
        'title',
        'code',
        'sec',
        'dive',
        'group',
        'class',
        'category',
        'desc',
    }
    assert feature_names == expected_features

    # Verify that the fix worked - all categorical values should be strings now
    for feature_metric in data_quality.feature_metrics:
        assert feature_metric.type == 'categorical'
        assert feature_metric.distinct_value > 0
