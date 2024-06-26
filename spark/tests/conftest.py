import os

import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_fixture():
    spark = SparkSession.builder.appName("Spark Session PyTest").getOrCreate()
    yield spark


@pytest.fixture(scope="session")
def test_data_dir():
    return os.path.join(os.path.dirname(__file__), "resources")
