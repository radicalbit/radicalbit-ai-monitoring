import pytest
from pyspark.sql import Row
from jobs.metrics.hellinger_distance import (
    HellingerDistance,
)
from tests.utils.pytest_utils import prefix_id

# from conftest import spark_fixture
import numpy as np


@pytest.fixture
def discrete_data(spark_fixture):
    """Fixture for creating discrete data as Spark DataFrames."""
    reference_data = spark_fixture.createDataFrame(
        [
            Row(category="A"),
            Row(category="A"),
            Row(category="B"),
            Row(category="B"),
            Row(category="B"),
            Row(category="C"),
        ]
    )

    current_data = spark_fixture.createDataFrame(
        [
            Row(category="A"),
            Row(category="B"),
            Row(category="B"),
            Row(category="C"),
            Row(category="C"),
            Row(category="C"),
        ]
    )

    return reference_data, current_data


@pytest.fixture
def continuous_data(spark_fixture):
    """Fixture for creating continuous data as Spark DataFrames."""
    reference_data = spark_fixture.createDataFrame(
        [Row(value=float(x)) for x in np.random.normal(0, 1, 100)]
    )

    current_data = spark_fixture.createDataFrame(
        [Row(value=float(x)) for x in np.random.normal(0.5, 1, 100)]
    )

    return reference_data, current_data


def test_hellinger_distance_discrete(spark_fixture, discrete_data):
    """Test Hellinger distance computation for discrete data."""
    reference_data, current_data = discrete_data
    hd = HellingerDistance(spark_fixture, reference_data, current_data, prefix_id)

    result = hd.compute_distance(on_column="category", data_type="discrete")

    assert "HellingerDistance" in result
    assert isinstance(result["HellingerDistance"], float)
    assert 0 <= result["HellingerDistance"] <= 1


def test_hellinger_distance_continuous(spark_fixture, continuous_data):
    """Test Hellinger distance computation for continuous data."""
    reference_data, current_data = continuous_data
    hd = HellingerDistance(spark_fixture, reference_data, current_data, prefix_id)

    result = hd.compute_distance(on_column="value", data_type="continuous")

    assert "HellingerDistance" in result
    assert isinstance(result["HellingerDistance"], float)
    assert 0 <= result["HellingerDistance"] <= 1


def test_invalid_data_type(spark_fixture, discrete_data):
    """Test handling of invalid data type."""
    reference_data, current_data = discrete_data
    hd = HellingerDistance(spark_fixture, reference_data, current_data, prefix_id)

    result = hd.compute_distance(on_column="category", data_type="invalid")

    assert result["HellingerDistance"] is None
