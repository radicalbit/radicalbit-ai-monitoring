import datetime
import uuid

from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
import pytest
from utils.models import (
    ColumnDefinition,
    DataType,
    FieldTypes,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)

from tests.utils.pytest_utils import prefix_id


@pytest.fixture
def dataset_target_string(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/multiclass/dataset_target_string_missing_classes.csv',
            header=True,
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/multiclass/dataset_target_string.csv',
            header=True,
        ),
    )


@pytest.fixture
def dataset_indexing(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/multiclass/dataset_target_int_indexing.csv',
            header=True,
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/current/multiclass/dataset_target_int_indexing.csv',
            header=True,
        ),
    )


def test_indexer(spark_fixture, dataset_target_string):
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

    current_dataframe, reference_dataframe = dataset_target_string
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=current_dataframe, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_dataframe, prefix_id=prefix_id
    )

    index_label_map, indexed_dataset = current_dataset.get_string_indexed_dataframe(
        reference_dataset
    )

    assert index_label_map == {
        '0.0': 'HEALTHY',
        '1.0': 'ORPHAN',
        '2.0': 'UNHEALTHY',
        '3.0': 'UNKNOWN',
    }


def test_indexer_numbers(spark_fixture, dataset_indexing):
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

    current_dataframe, reference_dataframe = dataset_indexing
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=current_dataframe, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_dataframe, prefix_id=prefix_id
    )

    index_label_map, indexed_dataset = current_dataset.get_string_indexed_dataframe(
        reference_dataset
    )

    assert index_label_map == {
        '0.0': '0',
        '1.0': '1',
        '2.0': '2',
        '3.0': '3',
        '4.0': '11',
    }
