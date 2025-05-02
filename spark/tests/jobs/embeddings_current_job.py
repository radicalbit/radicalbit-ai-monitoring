import logging

import pytest

from jobs.embeddings_current_job import compute_metrics
from jobs.utils.logger import logger_config

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


@pytest.fixture
def embeddings_reference(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True
    )


@pytest.fixture
def embeddings_current(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True
    )


def test_compute_results(spark_fixture, embeddings_reference, embeddings_current):
    r = compute_metrics(spark_fixture, embeddings_reference, embeddings_current)
    assert r["drift_score"]["score"] == 0.0
