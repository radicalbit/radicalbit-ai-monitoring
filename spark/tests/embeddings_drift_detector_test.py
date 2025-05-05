from deepdiff import DeepDiff
from embeddings.embeddings_metrics_calculator import EmbeddingsMetricsCalculator
from metrics.drift_calculator import DriftCalculator
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
    assert not DeepDiff(
        res,
        ref_metrics,
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
