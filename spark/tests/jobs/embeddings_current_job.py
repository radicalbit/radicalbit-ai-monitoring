import json
import logging

import pytest

from jobs.embeddings_current_job import compute_metrics
from jobs.utils.logger import logger_config

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


@pytest.fixture
def embeddings(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True
    )


@pytest.fixture
def embeddings_reference(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings_ref.csv', inferSchema=True, header=True
    )


@pytest.fixture
def embeddings_current(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/current/embeddings_cur.csv', inferSchema=True, header=True
    )


def test_compute_results_equal(spark_fixture, embeddings):
    r = compute_metrics(spark_fixture, embeddings, embeddings)
    drift_score = json.loads(r['DRIFT_SCORE'])
    assert isinstance(drift_score, float)
    assert drift_score == 0.0


def test_compute_results_diff(spark_fixture, embeddings_reference, embeddings_current):
    r = compute_metrics(spark_fixture, embeddings_reference, embeddings_current)
    drift_score = json.loads(r['DRIFT_SCORE'])
    assert isinstance(drift_score, float)
    assert drift_score > 0
