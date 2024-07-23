import datetime
import uuid
import pytest
import deepdiff

from current_job import compute_metrics as cur_compute_metrics
from reference_job import compute_metrics as ref_compute_metrics
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from utils.models import (
    ColumnDefinition,
    DataType,
    Granularity,
    ModelOut,
    ModelType,
    OutputType,
    SupportedTypes,
)
import tests.results.jobs_results as res


@pytest.fixture()
def reg_current_test_abalone(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/regression/regression_abalone_current1.csv",
            header=True,
        )
    )


@pytest.fixture()
def reg_reference_test_abalone(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/regression/regression_abalone_reference.csv",
            header=True,
        )
    )


@pytest.fixture()
def mc_reference_target_string(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/multiclass/dataset_target_string.csv",
            header=True,
        )
    )


@pytest.fixture()
def mc_current_target_string(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/multiclass/dataset_target_string.csv",
            header=True,
        )
    )


@pytest.fixture()
def bc_current_joined(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/current/current_joined.csv", header=True
        )
    )


@pytest.fixture()
def bc_reference_joined(spark_fixture, test_data_dir):
    yield (
        spark_fixture.read.csv(
            f"{test_data_dir}/reference/reference_joined.csv", header=True
        )
    )


@pytest.fixture()
def reg_model_abalone():
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
def mc_model_target_string():
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.string),
        prediction_proba=None,
        output=[ColumnDefinition(name="prediction", type=SupportedTypes.string)],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.string)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="cat1", type=SupportedTypes.string),
        ColumnDefinition(name="cat2", type=SupportedTypes.string),
        ColumnDefinition(name="num1", type=SupportedTypes.float),
        ColumnDefinition(name="num2", type=SupportedTypes.float),
    ]
    yield ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.MULTI_CLASS,
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
def bc_model_joined():
    output = OutputType(
        prediction=ColumnDefinition(name="prediction", type=SupportedTypes.float),
        prediction_proba=ColumnDefinition(
            name="prediction_proba", type=SupportedTypes.float
        ),
        output=[
            ColumnDefinition(name="prediction", type=SupportedTypes.float),
            ColumnDefinition(name="prediction_proba", type=SupportedTypes.float),
        ],
    )
    target = ColumnDefinition(name="target", type=SupportedTypes.float)
    timestamp = ColumnDefinition(name="datetime", type=SupportedTypes.datetime)
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(name="age", type=SupportedTypes.int),
        ColumnDefinition(name="sex", type=SupportedTypes.string),
        ColumnDefinition(name="chest_pain_type", type=SupportedTypes.int),
        ColumnDefinition(name="resting_blood_pressure", type=SupportedTypes.int),
        ColumnDefinition(name="cholesterol", type=SupportedTypes.int),
        ColumnDefinition(name="fasting_blood_sugar", type=SupportedTypes.int),
        ColumnDefinition(name="resting_ecg", type=SupportedTypes.int),
        ColumnDefinition(name="max_heart_rate_achieved", type=SupportedTypes.int),
        ColumnDefinition(name="exercise_induced_angina", type=SupportedTypes.int),
        ColumnDefinition(name="st_depression", type=SupportedTypes.float),
        ColumnDefinition(name="st_slope", type=SupportedTypes.int),
    ]
    yield ModelOut(
        uuid=uuid.uuid4(),
        name="model",
        description="description",
        model_type=ModelType.BINARY,
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
def reg_current_dataset_abalone(reg_current_test_abalone, reg_model_abalone):
    yield CurrentDataset(
        raw_dataframe=reg_current_test_abalone,
        model=reg_model_abalone,
    )


@pytest.fixture()
def reg_reference_dataset_abalone(reg_reference_test_abalone, reg_model_abalone):
    yield ReferenceDataset(
        raw_dataframe=reg_reference_test_abalone,
        model=reg_model_abalone,
    )


@pytest.fixture()
def mc_current_dataset_target_string(mc_current_target_string, mc_model_target_string):
    yield CurrentDataset(
        raw_dataframe=mc_current_target_string,
        model=mc_model_target_string,
    )


@pytest.fixture()
def mc_reference_dataset_target_string(
    mc_reference_target_string, mc_model_target_string
):
    yield ReferenceDataset(
        raw_dataframe=mc_reference_target_string,
        model=mc_model_target_string,
    )


@pytest.fixture()
def bc_current_dataset_joined(bc_current_joined, bc_model_joined):
    yield CurrentDataset(
        raw_dataframe=bc_current_joined,
        model=bc_model_joined,
    )


@pytest.fixture()
def bc_reference_dataset_joined(bc_reference_joined, bc_model_joined):
    yield ReferenceDataset(
        raw_dataframe=bc_reference_joined,
        model=bc_model_joined,
    )


def test_reg_abalone(
    spark_fixture,
    reg_current_dataset_abalone,
    reg_reference_dataset_abalone,
    reg_model_abalone,
):
    cur_record = cur_compute_metrics(
        spark_fixture,
        reg_current_dataset_abalone,
        reg_reference_dataset_abalone,
        reg_model_abalone,
    )
    ref_record = ref_compute_metrics(reg_reference_dataset_abalone, reg_model_abalone)

    assert not deepdiff.DeepDiff(
        cur_record,
        res.test_reg_abalone_current_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )

    assert not deepdiff.DeepDiff(
        ref_record,
        res.test_reg_abalone_reference_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_mc_target_string(
    spark_fixture,
    mc_current_dataset_target_string,
    mc_reference_dataset_target_string,
    mc_model_target_string,
):
    cur_record = cur_compute_metrics(
        spark_fixture,
        mc_current_dataset_target_string,
        mc_reference_dataset_target_string,
        mc_model_target_string,
    )
    ref_record = ref_compute_metrics(
        mc_reference_dataset_target_string, mc_model_target_string
    )

    assert not deepdiff.DeepDiff(
        cur_record,
        res.test_mc_target_string_current_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )

    assert not deepdiff.DeepDiff(
        ref_record,
        res.test_mc_target_string_reference_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )


def test_bc_joined(
    spark_fixture,
    bc_current_dataset_joined,
    bc_reference_dataset_joined,
    bc_model_joined,
):
    cur_record = cur_compute_metrics(
        spark_fixture,
        bc_current_dataset_joined,
        bc_reference_dataset_joined,
        bc_model_joined,
    )
    ref_record = ref_compute_metrics(bc_reference_dataset_joined, bc_model_joined)

    assert not deepdiff.DeepDiff(
        cur_record,
        res.test_bc_joined_current_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )

    assert not deepdiff.DeepDiff(
        ref_record,
        res.test_bc_joined_reference_res,
        ignore_order=True,
        ignore_type_subclasses=True,
    )
