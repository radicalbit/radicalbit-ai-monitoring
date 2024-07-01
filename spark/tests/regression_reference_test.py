import datetime
import uuid

import pytest

from jobs.utils.reference_regression import ReferenceMetricsRegressionService
from jobs.models.reference_dataset import ReferenceDataset
from jobs.utils.models import (
    ModelOut,
    ModelType,
    DataType,
    OutputType,
    ColumnDefinition,
    SupportedTypes,
    Granularity,
)
from tests.utils.pytest_utils import my_approx


@pytest.fixture()
def reference_bike(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/reference_bike.csv", header=True
    )


def test_calculation_dataset_target_int(spark_fixture, reference_bike):
    output = OutputType(
        prediction=ColumnDefinition(name="predictions", type=SupportedTypes.float),
        prediction_proba=None,
        output=[ColumnDefinition(name="predictions", type=SupportedTypes.float)],
    )
    target = ColumnDefinition(name="ground_truth", type=SupportedTypes.int)
    timestamp = ColumnDefinition(name="dteday", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="season", type=SupportedTypes.int),
        ColumnDefinition(name="yr", type=SupportedTypes.int),
        ColumnDefinition(name="mnth", type=SupportedTypes.int),
        ColumnDefinition(name="holiday", type=SupportedTypes.int),
        ColumnDefinition(name="weekday", type=SupportedTypes.int),
        ColumnDefinition(name="workingday", type=SupportedTypes.int),
        ColumnDefinition(name="weathersit", type=SupportedTypes.float),
        ColumnDefinition(name="temp", type=SupportedTypes.float),
        ColumnDefinition(name="atemp", type=SupportedTypes.float),
        ColumnDefinition(name="hum", type=SupportedTypes.float),
        ColumnDefinition(name="windspeed", type=SupportedTypes.float),
        ColumnDefinition(name="instant", type=SupportedTypes.int),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name="regression model",
        description="description",
        model_type=ModelType.REGRESSION,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks="framework",
        algorithm="algorithm",
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    reference_dataset = ReferenceDataset(
        raw_dataframe=reference_bike,
        model=model,
    )
    assert reference_dataset.reference_count == 731

    regression_service = ReferenceMetricsRegressionService(reference=reference_dataset)
    model_quality_metrics = regression_service.calculate_model_quality()

    expected = my_approx(
        {
            "mae": 126.6230232558139,
            "mape": 33.33458358635063,
            "mse": 42058.59416703146,
            "rmse": 205.08192062449447,
            "r2": 0.9106667318989127,
            "adj_r2": 0.9091736967774461,
            "var": 388091.1367098835,
        }
    )

    assert model_quality_metrics.model_dump() == expected
