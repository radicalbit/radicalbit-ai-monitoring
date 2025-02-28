import pytest
from pyspark.sql import DataFrame
from pyspark.sql import Row
from jobs.metrics.jensen_shannon_distance import JensenShannonDistance
from tests.utils.pytest_utils import prefix_id


@pytest.fixture(scope="module")
def reference_data(spark_fixture):
    """Fixture to create reference data for testing."""
    data = [
        Row(category="A", value=1.0),
        Row(category="B", value=2.0),
        Row(category="C", value=3.0),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def current_data(spark_fixture):
    """Fixture to create current data for testing."""
    data = [
        Row(category="A", value=1.5),
        Row(category="B", value=2.5),
        Row(category="C", value=3.5),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def jensen_shannon_distance(spark_fixture, reference_data, current_data):
    """Fixture to initialize the JensenShannonDistance class."""
    return JensenShannonDistance(
        spark_session=spark_fixture,
        reference_data=reference_data,
        current_data=current_data,
        prefix_id=prefix_id,
    )


def test_return_distance_discrete(jensen_shannon_distance):
    """Test the return_distance method for discrete data."""
    result = jensen_shannon_distance.compute_distance(
        on_column="category", data_type="discrete"
    )
    assert (
        "JensenShannonDistance" in result
    ), "The result should contain 'JensenShannonDistance'."
    assert (
        0 <= result["JensenShannonDistance"] <= 1
    ), "Distance should be between 0 and 1."


def test_calculate_category_percentages(jensen_shannon_distance):
    """Test the __calculate_category_percentages method."""
    percentages = (
        jensen_shannon_distance._JensenShannonDistance__calculate_category_percentages(
            df=jensen_shannon_distance.reference_data, column_name="category"
        )
    )
    assert isinstance(percentages, DataFrame), "Output should be a DataFrame."
    assert percentages.count() > 0, "Percentages should not be empty."
