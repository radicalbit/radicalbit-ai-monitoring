import datetime
import uuid
import pytest
import deepdiff

from metrics.statistics import calculate_statistics_current
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from utils.current_regression import CurrentMetricsRegressionService
from utils.models import (
    ColumnDefinition,
    DataType,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)
import tests.results.regression_current_results as res


@pytest.fixture()
def current_bike_dataframe(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/current/regression/bike.csv", header=True
    )


@pytest.fixture()
def reference_bike_dataframe(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/reference_bike.csv", header=True
    )


@pytest.fixture()
def current_test_fe(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/regression/regression_reference_test_FE.csv",
            header=True,
        )
    )


@pytest.fixture()
def reference_test_fe(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/regression/regression_reference_test_FE.csv",
            header=True,
        )
    )


@pytest.fixture()
def model():
    output = OutputType(
        prediction=ColumnDefinition(name="predictions", type=SupportedTypes.float),
        prediction_proba=None,
        output=[ColumnDefinition(name="predictions", type=SupportedTypes.float)],
    )
    target = ColumnDefinition(name="ground_truth", type=SupportedTypes.int)
    timestamp = ColumnDefinition(name="dteday", type=SupportedTypes.datetime)
    granularity = Granularity.MONTH
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
    ]
    yield ModelOut(
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


@pytest.fixture()
def model_test_fe():
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.int),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.int)],
    )
    target = ColumnDefinition(name="ground_truth", type=SupportedTypes.int)
    timestamp = ColumnDefinition(name="timestamp", type=SupportedTypes.datetime)
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(name="Sex", type=SupportedTypes.string),
        ColumnDefinition(name="Length", type=SupportedTypes.float),
        ColumnDefinition(name="Diameter", type=SupportedTypes.float),
        ColumnDefinition(name="Height", type=SupportedTypes.float),
        ColumnDefinition(name="Whole_weight", type=SupportedTypes.float),
        ColumnDefinition(name="Shucked_weight", type=SupportedTypes.float),
        ColumnDefinition(name="Viscera_weight", type=SupportedTypes.float),
        ColumnDefinition(name="Shell_weight", type=SupportedTypes.float),
        ColumnDefinition(name="pred_id", type=SupportedTypes.string),
    ]
    yield ModelOut(
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


@pytest.fixture()
def current_dataset_fe(current_test_fe, model_test_fe):
    yield CurrentDataset(
        raw_dataframe=current_test_fe,
        model=model_test_fe,
    )


@pytest.fixture()
def reference_dataset_fe(reference_test_fe, model_test_fe):
    yield ReferenceDataset(
        raw_dataframe=reference_test_fe,
        model=model_test_fe,
    )


@pytest.fixture()
def current_dataset(current_bike_dataframe, model):
    yield CurrentDataset(
        raw_dataframe=current_bike_dataframe,
        model=model,
    )


@pytest.fixture()
def reference_dataset(reference_bike_dataframe, model):
    yield ReferenceDataset(
        raw_dataframe=reference_bike_dataframe,
        model=model,
    )


def test_current_statistics(current_dataset):
    stats = calculate_statistics_current(current_dataset)

    assert current_dataset.current_count == stats.n_observations

    assert stats.missing_cells_perc == 100 * stats.missing_cells / (
        stats.n_variables * stats.n_observations
    )

    expected = res.test_current_statistics_res

    assert stats.model_dump(serialize_as_any=True) == expected


def test_data_quality(spark_fixture, current_dataset, reference_dataset):
    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    data_quality = metrics_service.calculate_data_quality(is_current=True)
    computed = data_quality.model_dump(serialize_as_any=True, exclude_none=True)

    features = res.test_data_quality_res["feature_metrics"]
    target = res.test_data_quality_res["target_metrics"]

    computed_features = computed["feature_metrics"]
    computed_target = computed["target_metrics"]

    assert not deepdiff.DeepDiff(
        computed_features,
        features,
        ignore_order=True,
        ignore_type_subclasses=True,
    )

    assert not deepdiff.DeepDiff(
        computed_target,
        target,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_model_quality(spark_fixture, current_dataset, reference_dataset):
    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    model_quality = metrics_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_model_quality_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_model_quality_test_fe(spark_fixture, current_dataset_fe, reference_dataset_fe):
    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset_fe,
        reference=reference_dataset_fe,
    )

    model_quality = metrics_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_model_quality_test_fe_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_drift_regression(spark_fixture, current_dataset, reference_dataset):
    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
    )

    drift = metrics_service.calculate_drift()

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_regression_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_drift_regression_chi(spark_fixture, current_dataset_fe, reference_dataset_fe):
    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset_fe,
        reference=reference_dataset_fe,
    )

    drift = metrics_service.calculate_drift()

    assert not deepdiff.DeepDiff(
        drift,
        res.test_drift_regression_chi,
        ignore_order=True,
        ignore_type_subclasses=True,
    )
