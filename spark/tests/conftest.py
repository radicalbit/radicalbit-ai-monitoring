import os

from pyspark.sql import SparkSession
import pytest


@pytest.fixture(scope='session')
def spark_fixture():
    return SparkSession.builder.appName('Spark Session PyTest').getOrCreate()


@pytest.fixture(scope='session')
def test_data_dir():
    return os.path.join(os.path.dirname(__file__), 'resources')
