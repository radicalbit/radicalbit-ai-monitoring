from pyspark.sql import DataFrame, Row
from pyspark.sql.types import DoubleType, StructField, StructType
import pytest
from utils.models import FieldTypes

from jobs.metrics.jensen_shannon_distance import JensenShannonDistance
from tests.resources.embeddings_distances import d
from tests.utils.pytest_utils import prefix_id


@pytest.fixture(scope='module')
def reference_data(spark_fixture):
    """Fixture to create reference data for testing."""
    data = [
        Row(category='A', value=1.0),
        Row(category='B', value=2.0),
        Row(category='C', value=3.0),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope='module')
def current_data(spark_fixture):
    """Fixture to create current data for testing."""
    data = [
        Row(category='A', value=1.5),
        Row(category='B', value=2.5),
        Row(category='C', value=3.5),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope='module')
def jensen_shannon_distance(spark_fixture, reference_data, current_data):
    """Fixture to initialize the JensenShannonDistance class."""
    return JensenShannonDistance(
        spark_session=spark_fixture,
        reference_data=reference_data,
        current_data=current_data,
        prefix_id=prefix_id,
    )


@pytest.fixture(scope='module')
def ref_distances(spark_fixture):
    schema = StructType(
        [StructField(name='distance', dataType=DoubleType(), nullable=True)]
    )
    return spark_fixture.createDataFrame(
        data=[(f,) for f in d['distances_ref']], schema=schema
    )


@pytest.fixture(scope='module')
def cur_distances(spark_fixture):
    schema = StructType(
        [StructField(name='distance', dataType=DoubleType(), nullable=True)]
    )
    return spark_fixture.createDataFrame(
        data=[(f,) for f in d['distances_cur']], schema=schema
    )


def test_return_distance_discrete(jensen_shannon_distance):
    """Test the return_distance method for discrete data."""
    result = jensen_shannon_distance.compute_distance(
        on_column='category', data_type=FieldTypes.categorical
    )
    assert (
        'JensenShannonDistance' in result
    ), "The result should contain 'JensenShannonDistance'."
    assert (
        0 <= result['JensenShannonDistance'] <= 1
    ), 'Distance should be between 0 and 1.'


def test_return_distance_continous(jensen_shannon_distance):
    """Test the return_distance method for discrete data."""
    result = jensen_shannon_distance.compute_distance(
        on_column='value', data_type=FieldTypes.numerical
    )
    assert (
        'JensenShannonDistance' in result
    ), "The result should contain 'JensenShannonDistance'."
    assert (
        0 <= result['JensenShannonDistance'] <= 1
    ), 'Distance should be between 0 and 1.'


def test_calculate_category_percentages(jensen_shannon_distance):
    """Test the __calculate_category_percentages method."""
    percentages = (
        jensen_shannon_distance._JensenShannonDistance__calculate_category_percentages(
            df=jensen_shannon_distance.reference_data, column_name='category'
        )
    )
    assert isinstance(percentages, DataFrame), 'Output should be a DataFrame.'
    assert percentages.count() > 0, 'Percentages should not be empty.'


def test_compute_drift_embeddings(spark_fixture, ref_distances, cur_distances):
    js = JensenShannonDistance(spark_fixture, ref_distances, cur_distances, 'rb')
    d = js.compute_distance('distance', FieldTypes.numerical)
    assert d['JensenShannonDistance'] > 0
