import pytest
from pyspark.sql import Row
from jobs.metrics.wasserstein_distance import WassersteinDistance


@pytest.fixture(scope="module")
def reference_data(spark_fixture):
    """Fixture to create reference data for testing."""
    data = [
        Row(value=1.0),
        Row(value=2.0),
        Row(value=3.0),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def current_data(spark_fixture):
    """Fixture to create current data for testing."""
    data = [
        Row(value=1.5),
        Row(value=2.5),
        Row(value=3.5),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def categorical_data(spark_fixture):
    """Fixture to create categorical (string) data for testing."""
    data = [
        Row(value="A"),
        Row(value="B"),
        Row(value="C"),
    ]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def wasserstein_distance(spark_fixture, reference_data, current_data):
    """Fixture to initialize the WassersteinDistance class."""
    return WassersteinDistance(
        spark_session=spark_fixture,
        reference_data=reference_data,
        current_data=current_data,
    )


def test_return_distance(wasserstein_distance):
    """Test the return_distance method for Wasserstein Distance computation."""
    result = wasserstein_distance.compute_distance(on_column="value")
    assert (
        "WassersteinDistance" in result
    ), "The result should contain 'WassersteinDistance'."
    assert result["WassersteinDistance"] >= 0, "Distance should be non-negative."


def test_wasserstein_distance_on_categorical_data(spark_fixture, categorical_data):
    """Test that Wasserstein distance cannot be computed on categorical data."""
    wasserstein_distance = WassersteinDistance(
        spark_session=spark_fixture,
        reference_data=categorical_data,
        current_data=categorical_data,
    )

    with pytest.raises(Exception, match="could not convert string to float"):
        wasserstein_distance.compute_distance(on_column="value")
