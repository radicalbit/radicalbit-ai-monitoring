import pytest
from pyspark.sql import Row
from jobs.metrics.kullback_leibler_divergence import KullbackLeiblerDivergence
from tests.utils.pytest_utils import prefix_id
from utils.models import FieldTypes


@pytest.fixture(scope="module")
def reference_data_continuous(spark_fixture):
    """Fixture to create reference data with numerical values."""
    data = [Row(value=float(i)) for i in range(1, 15)]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def current_data_continuous(spark_fixture):
    """Fixture to create current data with numerical values."""
    data = [Row(value=float(i)) for i in range(1, 15)]
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def reference_data_categorical(spark_fixture):
    """Fixture to create reference data with categorical values."""
    data = [Row(value="A")] * 5 + [Row(value="B")] * 5 + [Row(value="C")] * 4
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def current_data_categorical(spark_fixture):
    """Fixture to create current data with categorical values."""
    data = [Row(value="A")] * 3 + [Row(value="B")] * 3 + [Row(value="C")] * 3
    return spark_fixture.createDataFrame(data)


@pytest.fixture(scope="module")
def kl_div_continuous(
    spark_fixture, reference_data_continuous, current_data_continuous
):
    """Fixture to initialize the KullbackLeiblerDivergence class for continuous data."""
    return KullbackLeiblerDivergence(
        spark_session=spark_fixture,
        reference_data=reference_data_continuous,
        current_data=current_data_continuous,
        prefix_id=prefix_id,
    )


@pytest.fixture(scope="module")
def kl_div_categorical(
    spark_fixture, reference_data_categorical, current_data_categorical
):
    """Fixture to initialize the KullbackLeiblerDivergence class for categorical data."""
    return KullbackLeiblerDivergence(
        spark_session=spark_fixture,
        reference_data=reference_data_categorical,
        current_data=current_data_categorical,
        prefix_id=prefix_id,
    )


def test_compute_distance_continuous(kl_div_continuous):
    """Test the computation of KL divergence for continuous data."""
    result = kl_div_continuous.compute_distance(
        on_column="value", data_type=FieldTypes.numerical
    )
    assert (
        "KullbackLeiblerDivergence" in result
    ), "The result should contain 'KullbackLeiblerDivergence'."
    assert (
        result["KullbackLeiblerDivergence"] is not None
    ), "KL divergence should be computed."


def test_compute_distance_categorical(kl_div_categorical):
    """Test the computation of KL divergence for categorical data."""
    result = kl_div_categorical.compute_distance(
        on_column="value", data_type=FieldTypes.categorical
    )
    assert (
        "KullbackLeiblerDivergence" in result
    ), "The result should contain 'KullbackLeiblerDivergence'."
    assert (
        result["KullbackLeiblerDivergence"] is not None
    ), "KL divergence should be computed."


def test_kl_divergence_zero_case(spark_fixture):
    """Test that KL divergence is zero when distributions are identical."""
    data = [Row(value="A")] * 5 + [Row(value="B")] * 5
    reference_data = spark_fixture.createDataFrame(data)
    current_data = spark_fixture.createDataFrame(data)

    kl_div = KullbackLeiblerDivergence(
        spark_session=spark_fixture,
        reference_data=reference_data,
        current_data=current_data,
        prefix_id="test",
    )

    result = kl_div.compute_distance(
        on_column="value", data_type=FieldTypes.categorical
    )
    assert (
        result["KullbackLeiblerDivergence"] == 0.0
    ), "KL divergence should be zero for identical distributions."


def test_kl_divergence_with_missing_category(spark_fixture, reference_data_categorical):
    """Test KL divergence when a category is missing in the current dataset."""
    current_data = spark_fixture.createDataFrame([Row(value="A")] * 5)  # Missing "B"

    kl_div = KullbackLeiblerDivergence(
        spark_session=spark_fixture,
        reference_data=reference_data_categorical,
        current_data=current_data,
        prefix_id="test",
    )

    result = kl_div.compute_distance(
        on_column="value", data_type=FieldTypes.categorical
    )
    assert (
        result["KullbackLeiblerDivergence"] is None
    ), "KL divergence should be None when a category has zero probability."
