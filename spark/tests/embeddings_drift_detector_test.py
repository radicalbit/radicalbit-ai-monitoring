
from embeddings.embeddings_drift_detector import EmbeddingsDriftDetector
import pytest

from tests.results.embedding_ref_metrics import ref_metrics


@pytest.fixture
def embeddings_dataset(spark_fixture, test_data_dir):
    return spark_fixture.read.csv(
        f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True
    )


def test_drift_detector(spark_fixture, embeddings_dataset):
    embedding_drift = EmbeddingsDriftDetector(
        spark_fixture, embeddings_dataset, '', 0.80
    )
    res = embedding_drift.compute_result()
    assert (
        res['reference_embeddings_metrics']['inertia']
        == ref_metrics['reference_embeddings_metrics']['inertia']
    )
    assert (
        res['reference_embeddings_metrics']['n_cluster']
        == ref_metrics['reference_embeddings_metrics']['n_cluster']
    )
    assert (
        res['reference_embeddings_metrics']['n_comp']
        == ref_metrics['reference_embeddings_metrics']['n_comp']
    )
    assert (
        res['reference_embeddings_metrics']['sil_score']
        == ref_metrics['reference_embeddings_metrics']['sil_score']
    )
    assert res['reference_embeddings'] == ref_metrics['reference_embeddings']
    assert res['histogram'] == ref_metrics['histogram']
