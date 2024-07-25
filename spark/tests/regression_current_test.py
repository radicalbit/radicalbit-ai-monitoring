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
    FieldTypes,
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
def current_test_abalone(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/regression/regression_abalone_current1.csv",
            header=True,
        )
    )


@pytest.fixture()
def reference_test_abalone(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/regression/regression_abalone_reference.csv",
            header=True,
        )
    )


@pytest.fixture()
def model():
    output = OutputType(
        prediction=ColumnDefinition(
            name="predictions",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name="predictions",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            )
        ],
    )
    target = ColumnDefinition(
        name="ground_truth", type=SupportedTypes.int, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="dteday", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(
            name="season", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="yr", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="mnth", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="holiday", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="weekday", type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="workingday",
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        ColumnDefinition(
            name="weathersit",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="temp", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="atemp", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="hum", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="windspeed", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
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
def model_test_abalone():
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction", type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.int,
                field_type=FieldTypes.numerical,
            )
        ],
    )
    target = ColumnDefinition(
        name="ground_truth", type=SupportedTypes.int, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="timestamp", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(
            name="Sex", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="Length", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="Diameter", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="Height", type=SupportedTypes.float, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="Whole_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="Shucked_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="Viscera_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="Shell_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="pred_id",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
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
def current_dataset_abalone(current_test_abalone, model_test_abalone):
    yield CurrentDataset(
        raw_dataframe=current_test_abalone,
        model=model_test_abalone,
    )


@pytest.fixture()
def reference_dataset_abalone(reference_test_abalone, model_test_abalone):
    yield ReferenceDataset(
        raw_dataframe=reference_test_abalone,
        model=model_test_abalone,
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
    print(computed)

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


def test_model_quality_abalone(
    spark_fixture, current_dataset_abalone, reference_dataset_abalone
):
    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset_abalone,
        reference=reference_dataset_abalone,
    )

    model_quality = metrics_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_model_quality_abalone_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )
