import pytest

from embeddings.embeddings_drift_detector import EmbeddingsDriftDetector


@pytest.fixture
def embeddings_dataset(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(f'{test_data_dir}/reference/embeddings.csv', inferSchema=True, header=True)
    )

def test_drift_detector(spark_fixture, embeddings_dataset):
    embedding_drift = EmbeddingsDriftDetector(
        spark_fixture, embeddings_dataset, '', 0.80
    )
    res = embedding_drift.compute_result()
    assert res is not None
    metrics = res["reference_embeddings_metrics"]
    histogram = res["histogram"]
    reference_embeddings = res['reference_embeddings']
    assert metrics["n_comp"] == 32
    assert metrics["n_cluster"] == 2
    assert metrics["inertia"] == 67839.95525645588
    assert metrics["sil_score"] == 0.09446819346116185
    assert histogram['buckets'] is not None
    assert histogram['reference_values'] is not None
    assert reference_embeddings["values"] is not None
    assert reference_embeddings["centroid"] == {"x": -0.0000000000000014210854715202005, "y": 0.00000000000000014802973661668753}

