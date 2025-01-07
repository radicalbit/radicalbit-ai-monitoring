import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from jobs.metrics.hellinger_distance import (
    HellingerDistance,
)  # Adjust import path as needed
import numpy as np


def create_spark_session():
    """Creates a local Spark session for testing."""
    return (
        SparkSession.builder.master("local[*]")
        .appName("HellingerDistanceTest")
        .getOrCreate()
    )


@pytest.fixture(scope="module")
def spark_session():
    """Fixture for Spark session."""
    spark = create_spark_session()
    yield spark
    spark.stop()


@pytest.fixture
def discrete_data(spark_session):
    """Fixture for creating discrete data as Spark DataFrames."""
    reference_data = spark_session.createDataFrame(
        [
            Row(category="A"),
            Row(category="A"),
            Row(category="B"),
            Row(category="B"),
            Row(category="B"),
            Row(category="C"),
        ]
    )

    current_data = spark_session.createDataFrame(
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
def continuous_data(spark_session):
    """Fixture for creating continuous data as Spark DataFrames."""
    reference_data = spark_session.createDataFrame(
        [Row(value=float(x)) for x in np.random.normal(0, 1, 100)]
    )

    current_data = spark_session.createDataFrame(
        [Row(value=float(x)) for x in np.random.normal(0.5, 1, 100)]
    )

    return reference_data, current_data


def test_hellinger_distance_discrete(spark_session, discrete_data):
    """Test Hellinger distance computation for discrete data."""
    reference_data, current_data = discrete_data
    hd = HellingerDistance(spark_session, reference_data, current_data)

    result = hd.return_distance(on_column="category", data_type="discrete")

    assert "HellingerDistance" in result
    assert isinstance(result["HellingerDistance"], float)
    assert 0 <= result["HellingerDistance"] <= 1


def test_hellinger_distance_continuous(spark_session, continuous_data):
    """Test Hellinger distance computation for continuous data."""
    reference_data, current_data = continuous_data
    hd = HellingerDistance(spark_session, reference_data, current_data)

    result = hd.return_distance(on_column="value", data_type="continuous")

    assert "HellingerDistance" in result
    assert isinstance(result["HellingerDistance"], float)
    assert 0 <= result["HellingerDistance"] <= 1


def test_invalid_data_type(spark_session, discrete_data):
    """Test handling of invalid data type."""
    reference_data, current_data = discrete_data
    hd = HellingerDistance(spark_session, reference_data, current_data)

    result = hd.return_distance(on_column="category", data_type="invalid")

    assert result["HellingerDistance"] is None
