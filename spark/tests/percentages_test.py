import datetime
import uuid

import deepdiff
from metrics.drift_calculator import DriftCalculator
from metrics.percentages import PercentageCalculator
import pytest
from utils.current_binary import CurrentMetricsService
from utils.current_multiclass import CurrentMetricsMulticlassService
from utils.current_regression import CurrentMetricsRegressionService
from utils.models import DriftAlgorithmType, DriftMethod

from jobs.models.current_dataset import CurrentDataset
from jobs.models.reference_dataset import ReferenceDataset
from jobs.utils.models import (
    ColumnDefinition,
    DataType,
    FieldTypes,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)
import tests.results.percentage_results as res
from tests.utils.pytest_utils import prefix_id

drift_chi2 = [DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05).model_dump()]
drift_ks = [DriftMethod(name=DriftAlgorithmType.KS, threshold=0.05).model_dump()]
drift_psi = [DriftMethod(name=DriftAlgorithmType.PSI, p_value=0.1).model_dump()]


@pytest.fixture
def test_dataset_abalone(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/regression/regression_abalone_current1.csv',
            header=True,
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/regression/regression_abalone_reference.csv',
            header=True,
        ),
    )


@pytest.fixture
def easy_dataset(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/current/easy_dataset.csv', header=True
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/easy_dataset.csv', header=True
        ),
    )


@pytest.fixture
def dataset_perfect_classes(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/multiclass/dataset_perfect_classes.csv',
            header=True,
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/current/multiclass/dataset_perfect_classes.csv',
            header=True,
        ),
    )


@pytest.fixture
def dataset_talk(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/multiclass/reference_sentiment_analysis_talk.csv',
            header=True,
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/current/multiclass/current_sentiment_analysis_talk.csv',
            header=True,
        ),
    )


@pytest.fixture
def dataset_demo(spark_fixture, test_data_dir):
    return (
        spark_fixture.read.csv(
            f'{test_data_dir}/reference/multiclass/3_classes_reference.csv',
            header=True,
        ),
        spark_fixture.read.csv(
            f'{test_data_dir}/current/multiclass/3_classes_current1.csv',
            header=True,
        ),
    )


def test_calculation_dataset_perfect_classes(spark_fixture, dataset_perfect_classes):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.string, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name='cat2',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name='num1',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='num2',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.MULTI_CLASS,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    current_dataframe, reference_dataframe = dataset_perfect_classes
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=current_dataframe, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=reference_dataframe, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality()

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id,
    )

    percentages = PercentageCalculator.calculate_percentages(
        spark_session=spark_fixture,
        drift=drift,
        model_quality_current=model_quality,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
        prefix_id=prefix_id,
    )
    assert not deepdiff.DeepDiff(
        percentages,
        res.test_percentage_perfect_classes,
        ignore_order=True,
        significant_digits=6,
    )


def test_percentage_easy_dataset(spark_fixture, easy_dataset):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name='prediction_proba',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name='prediction_proba',
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name='target', type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='datetime', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='cat1',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name='cat2',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name='num1',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='num2',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='model',
        description='description',
        model_type=ModelType.BINARY,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = easy_dataset
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    metrics_service = CurrentMetricsService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()

    percentages = PercentageCalculator.calculate_percentages(
        spark_session=spark_fixture,
        drift=drift,
        model_quality_current=model_quality,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
        prefix_id=prefix_id,
    )
    assert not deepdiff.DeepDiff(
        percentages,
        res.test_percentage_easy_dataset,
        ignore_order=True,
        significant_digits=6,
    )


def test_percentages_abalone(spark_fixture, test_dataset_abalone):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction', type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.int,
                field_type=FieldTypes.numerical,
            )
        ],
    )
    target = ColumnDefinition(
        name='ground_truth', type=SupportedTypes.int, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name='timestamp', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.MONTH
    features = [
        ColumnDefinition(
            name='Sex',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name='Length',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='Diameter',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='Height',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='Whole_weight',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='Shucked_weight',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='Viscera_weight',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='Shell_weight',
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name='pred_id',
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='regression model',
        description='description',
        model_type=ModelType.REGRESSION,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_current_dataset, raw_reference_dataset = test_dataset_abalone
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id,
    )

    metrics_service = CurrentMetricsRegressionService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality()

    percentages = PercentageCalculator.calculate_percentages(
        spark_session=spark_fixture,
        drift=drift,
        model_quality_current=model_quality,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
        prefix_id=prefix_id,
    )

    assert not deepdiff.DeepDiff(
        percentages,
        res.test_percentage_abalone,
        ignore_order=True,
        significant_digits=6,
    )


def test_percentages_dataset_talk(spark_fixture, dataset_talk):
    output = OutputType(
        prediction=ColumnDefinition(
            name='content', type=SupportedTypes.int, field_type=FieldTypes.categorical
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='content',
                type=SupportedTypes.int,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='label', type=SupportedTypes.int, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name='rbit_prediction_ts',
        type=SupportedTypes.datetime,
        field_type=FieldTypes.datetime,
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name='total_tokens',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name='prompt_tokens',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='talk model',
        description='description',
        model_type=ModelType.MULTI_CLASS,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_reference_dataset, raw_current_dataset = dataset_talk
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id,
    )

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality()

    percentages = PercentageCalculator.calculate_percentages(
        spark_session=spark_fixture,
        drift=drift,
        model_quality_current=model_quality,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
        prefix_id=prefix_id,
    )

    assert not deepdiff.DeepDiff(
        percentages,
        res.test_dataset_talk,
        ignore_order=True,
        significant_digits=6,
    )


def test_percentages_dataset_demo(spark_fixture, dataset_demo):
    output = OutputType(
        prediction=ColumnDefinition(
            name='prediction',
            type=SupportedTypes.int,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name='prediction',
                type=SupportedTypes.int,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name='ground_truth', type=SupportedTypes.int, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name='timestamp', type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.DAY
    features = [
        ColumnDefinition(
            name='age', type=SupportedTypes.int, field_type=FieldTypes.numerical
        )
    ]
    model = ModelOut(
        uuid=uuid.uuid4(),
        name='talk model',
        description='description',
        model_type=ModelType.MULTI_CLASS,
        data_type=DataType.TABULAR,
        timestamp=timestamp,
        granularity=granularity,
        outputs=output,
        target=target,
        features=features,
        frameworks='framework',
        algorithm='algorithm',
        created_at=str(datetime.datetime.now()),
        updated_at=str(datetime.datetime.now()),
    )

    raw_reference_dataset, raw_current_dataset = dataset_demo
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current_dataset, prefix_id=prefix_id
    )
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference_dataset, prefix_id=prefix_id
    )

    drift = DriftCalculator.calculate_drift(
        spark_session=spark_fixture,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        prefix_id=prefix_id,
    )

    metrics_service = CurrentMetricsMulticlassService(
        spark_session=spark_fixture,
        current=current_dataset,
        reference=reference_dataset,
        prefix_id=prefix_id,
    )

    model_quality = metrics_service.calculate_model_quality()

    percentages = PercentageCalculator.calculate_percentages(
        spark_session=spark_fixture,
        drift=drift,
        model_quality_current=model_quality,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
        prefix_id=prefix_id,
    )

    assert not deepdiff.DeepDiff(
        percentages,
        res.test_dataset_demo,
        ignore_order=True,
        significant_digits=6,
    )
