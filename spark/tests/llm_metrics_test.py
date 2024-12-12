import pytest
import orjson
from jobs.llm_job import compute_metrics
from jobs.metrics.llm_metrics import LLMMetrics
from jobs.models.llm_dataset import LLMMetricsModel
from tests.results.llm_metrics_results import llm_metric_results
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_response(spark_fixture, test_data_dir):
    yield spark_fixture.read.option("multiline", "true").json(
        f"{test_data_dir}/llm/metrics.json"
    )


def test_remove_columns(spark_fixture, mock_response):
    llm_metrics_service = LLMMetrics()
    df = llm_metrics_service.remove_columns(mock_response)
    assert "id" in df.columns
    assert "choices" in df.columns
    assert len(df.columns) == 2


def test_compute_prob(spark_fixture, mock_response):
    llm_metrics_service = LLMMetrics()
    df = llm_metrics_service.remove_columns(mock_response)
    df = llm_metrics_service.compute_prob(df)
    assert {"id", "logprob", "token", "prob"} == set(df.columns)
    assert not df.rdd.isEmpty()


def test_extract_metrics(spark_fixture, mock_response):
    llm_metrics_service = LLMMetrics()
    llm_metrics_model = llm_metrics_service.extract_metrics(mock_response)
    assert isinstance(llm_metrics_model, LLMMetricsModel)


def test_compute_metrics(spark_fixture, mock_response):
    complete_record = compute_metrics(mock_response)
    model_quality = complete_record.get("MODEL_QUALITY")
    assert model_quality == orjson.dumps(llm_metric_results).decode("utf-8")
