import pytest
import orjson
from jobs.completion_job import compute_metrics
from jobs.metrics.completion_metrics import CompletionMetrics
from jobs.models.completion_dataset import CompletionMetricsModel
from tests.results.completion_metrics_results import completion_metric_results


@pytest.fixture
def input_file(spark_fixture, test_data_dir):
    yield spark_fixture.read.option("multiline", "true").json(
        f"{test_data_dir}/completion/metrics.json"
    )


def test_remove_columns(spark_fixture, input_file):
    completion_metrics_service = CompletionMetrics()
    df = completion_metrics_service.remove_columns(input_file)
    assert "id" in df.columns
    assert "choices" in df.columns
    assert len(df.columns) == 2


def test_compute_prob(spark_fixture, input_file):
    completion_metrics_service = CompletionMetrics()
    df = completion_metrics_service.remove_columns(input_file)
    df = completion_metrics_service.compute_prob(df)
    assert {"id", "logprob", "token", "prob"} == set(df.columns)
    assert not df.rdd.isEmpty()


def test_extract_metrics(spark_fixture, input_file):
    completion_metrics_service = CompletionMetrics()
    completion_metrics_model: CompletionMetricsModel = completion_metrics_service.extract_metrics(input_file)
    assert len(completion_metrics_model.tokens) > 0
    assert len(completion_metrics_model.mean_per_phrase) > 0
    assert len(completion_metrics_model.mean_per_file) > 0


def test_compute_metrics(spark_fixture, input_file):
    complete_record = compute_metrics(input_file)
    model_quality = complete_record.get("MODEL_QUALITY")
    assert model_quality == orjson.dumps(completion_metric_results).decode(
        "utf-8"
    )
