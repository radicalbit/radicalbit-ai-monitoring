from deepdiff import DeepDiff
from embeddings.embeddings_metrics_calculator import EmbeddingsMetricsCalculator
from metrics.drift_calculator import DriftCalculator
from numpy.testing import assert_allclose
from pyspark.sql.types import DoubleType, StructField, StructType
import pytest

from tests.results.embedding_ref_metrics import ref_metrics


@pytest.fixture
def embeddings_dataset(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True
    )


@pytest.fixture
def embeddings_dataset_v2(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True
    )


def test_drift_detector(spark_fixture, embeddings_dataset):
    embedding_drift = EmbeddingsMetricsCalculator(
        spark_fixture, embeddings_dataset, '', 0.80
    )
    res = embedding_drift.compute_result()
    assert_allclose(
        res['embeddings_metrics']['inertia'],
        ref_metrics['embeddings_metrics']['inertia'],
        rtol=1e-07,
        atol=0,
    )
    assert_allclose(
        res['embeddings_metrics']['n_cluster'],
        ref_metrics['embeddings_metrics']['n_cluster'],
        rtol=1e-07,
        atol=0,
    )
    assert_allclose(
        res['embeddings_metrics']['n_comp'],
        ref_metrics['embeddings_metrics']['n_comp'],
        rtol=1e-07,
        atol=0,
    )
    assert_allclose(
        res['embeddings_metrics']['sil_score'],
        ref_metrics['embeddings_metrics']['sil_score'],
        rtol=1e-07,
        atol=0,
    )
    assert DeepDiff(
        res['embeddings'],
        ref_metrics['embeddings'],
        ignore_order=True,
        significant_digits=6,
    )
    assert DeepDiff(
        res['histogram'],
        ref_metrics['histogram'],
        ignore_order=True,
        significant_digits=6,
    )


def test_drift_detection(spark_fixture):
    ref_embeddings_dataset = ref_metrics['histogram']['distances']
    cur_emdeddings_drift = ref_metrics['histogram']['distances']
    schema = StructType(
        [StructField(name='distance', dataType=DoubleType(), nullable=True)]
    )
    drift_score = DriftCalculator.calculate_embeddings_drift(
        spark_fixture,
        spark_fixture.createDataFrame(
            data=[(f,) for f in ref_embeddings_dataset], schema=schema
        ),
        spark_fixture.createDataFrame(
            data=[(f,) for f in cur_emdeddings_drift], schema=schema
        ),
        'rb',
    )
    assert drift_score == 0
