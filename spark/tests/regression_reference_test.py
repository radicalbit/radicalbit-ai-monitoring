import datetime
import uuid

import pytest
import deepdiff

from jobs.metrics.statistics import calculate_statistics_reference
from jobs.utils.reference_regression import ReferenceMetricsRegressionService
from jobs.models.reference_dataset import ReferenceDataset
from jobs.utils.models import (
    ModelOut,
    ModelType,
    DataType,
    OutputType,
    ColumnDefinition,
    SupportedTypes,
    FieldTypes,
    Granularity,
)
from tests.utils.pytest_utils import my_approx, prefix_id
import tests.results.regression_reference_results as res


@pytest.fixture()
def reference_bike(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/reference_bike.csv", header=True
    )


@pytest.fixture()
def reference_bike_nulls(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/reference_bike_nulls.csv", header=True
    )


@pytest.fixture()
def reference_abalone(spark_fixture, test_data_dir):
    yield spark_fixture.read.csv(
        f"{test_data_dir}/reference/regression/regression_abalone_reference.csv",
        header=True,
    )


@pytest.fixture()
def reference_dataset(reference_bike):
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
    granularity = Granularity.HOUR
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

    yield ReferenceDataset(
        raw_dataframe=reference_bike, model=model, prefix_id=prefix_id
    )


@pytest.fixture()
def reference_dataset_nulls(spark_fixture, reference_bike_nulls):
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
    granularity = Granularity.HOUR
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

    yield ReferenceDataset(
        raw_dataframe=reference_bike_nulls, model=model, prefix_id=prefix_id
    )


@pytest.fixture()
def reference_dataset_abalone(spark_fixture, reference_abalone):
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

    yield ReferenceDataset(
        raw_dataframe=reference_abalone, model=model, prefix_id=prefix_id
    )


def test_model_quality_metrics(reference_dataset):
    assert reference_dataset.reference_count == 731

    regression_service = ReferenceMetricsRegressionService(
        reference=reference_dataset, prefix_id=prefix_id
    )
    model_quality_metrics = regression_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality_metrics,
        res.test_model_quality_metrics_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_model_quality_abalone(reference_dataset_abalone):
    metrics_service = ReferenceMetricsRegressionService(
        reference=reference_dataset_abalone, prefix_id=prefix_id
    )

    model_quality = metrics_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality,
        res.test_model_quality_abalone_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_statistics_metrics(reference_dataset):
    stats = calculate_statistics_reference(reference_dataset)
    expected = my_approx(res.test_statistics_metrics_res)

    assert stats.model_dump(serialize_as_any=True) == expected


def test_data_quality_metrics(reference_dataset):
    regression_service = ReferenceMetricsRegressionService(
        reference=reference_dataset, prefix_id=prefix_id
    )
    data_quality = regression_service.calculate_data_quality()

    features = res.test_data_quality_metrics_res["feature_metrics"]
    target = res.test_data_quality_metrics_res["target_metrics"]

    computed = data_quality.model_dump(serialize_as_any=True, exclude_none=True)

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


def test_model_quality_metrics_nulls(reference_dataset_nulls):
    regression_service = ReferenceMetricsRegressionService(
        reference=reference_dataset_nulls, prefix_id=prefix_id
    )
    model_quality_metrics = regression_service.calculate_model_quality()

    assert not deepdiff.DeepDiff(
        model_quality_metrics,
        res.test_model_quality_metrics_nulls_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )
