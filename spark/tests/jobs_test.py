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
    FieldTypes,
    DriftAlgorithmType,
    DriftMethod,
)
import tests.results.jobs_results as res
from tests.utils.pytest_utils import prefix_id

drift_chi2 = [DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05).model_dump()]
drift_ks = [DriftMethod(name=DriftAlgorithmType.KS, p_value=0.05).model_dump()]
drift_psi = [DriftMethod(name=DriftAlgorithmType.PSI, threshold=0.1).model_dump()]


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
            name="Sex",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name="Length",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name="Diameter",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name="Height",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name="Whole_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name="Shucked_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name="Viscera_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name="Shell_weight",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name="pred_id",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
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
def mc_model_target_string():
    output = OutputType(
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
        ),
        prediction_proba=None,
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.string,
                field_type=FieldTypes.categorical,
            )
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.string, field_type=FieldTypes.categorical
    )
    timestamp = ColumnDefinition(
        name="datetime", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="cat1",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name="cat2",
            type=SupportedTypes.string,
            field_type=FieldTypes.categorical,
            drift=drift_chi2,
        ),
        ColumnDefinition(
            name="num1",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
        ColumnDefinition(
            name="num2",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
            drift=drift_ks,
        ),
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
        prediction=ColumnDefinition(
            name="prediction",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        prediction_proba=ColumnDefinition(
            name="prediction_proba",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        output=[
            ColumnDefinition(
                name="prediction",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
            ColumnDefinition(
                name="prediction_proba",
                type=SupportedTypes.float,
                field_type=FieldTypes.numerical,
            ),
        ],
    )
    target = ColumnDefinition(
        name="target", type=SupportedTypes.float, field_type=FieldTypes.numerical
    )
    timestamp = ColumnDefinition(
        name="datetime", type=SupportedTypes.datetime, field_type=FieldTypes.datetime
    )
    granularity = Granularity.HOUR
    features = [
        ColumnDefinition(
            name="age", type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="sex", type=SupportedTypes.string, field_type=FieldTypes.categorical
        ),
        ColumnDefinition(
            name="chest_pain_type",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="resting_blood_pressure",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="cholesterol", type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="fasting_blood_sugar",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="resting_ecg", type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
        ColumnDefinition(
            name="max_heart_rate_achieved",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="exercise_induced_angina",
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="st_depression",
            type=SupportedTypes.float,
            field_type=FieldTypes.numerical,
        ),
        ColumnDefinition(
            name="st_slope", type=SupportedTypes.int, field_type=FieldTypes.numerical
        ),
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
        prefix_id=prefix_id,
    )


@pytest.fixture()
def reg_reference_dataset_abalone(reg_reference_test_abalone, reg_model_abalone):
    yield ReferenceDataset(
        raw_dataframe=reg_reference_test_abalone,
        model=reg_model_abalone,
        prefix_id=prefix_id,
    )


@pytest.fixture()
def mc_current_dataset_target_string(mc_current_target_string, mc_model_target_string):
    yield CurrentDataset(
        raw_dataframe=mc_current_target_string,
        model=mc_model_target_string,
        prefix_id=prefix_id,
    )


@pytest.fixture()
def mc_reference_dataset_target_string(
    mc_reference_target_string, mc_model_target_string
):
    yield ReferenceDataset(
        raw_dataframe=mc_reference_target_string,
        model=mc_model_target_string,
        prefix_id=prefix_id,
    )


@pytest.fixture()
def bc_current_dataset_joined(bc_current_joined, bc_model_joined):
    yield CurrentDataset(
        raw_dataframe=bc_current_joined, model=bc_model_joined, prefix_id=prefix_id
    )


@pytest.fixture()
def bc_reference_dataset_joined(bc_reference_joined, bc_model_joined):
    yield ReferenceDataset(
        raw_dataframe=bc_reference_joined, model=bc_model_joined, prefix_id=prefix_id
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
        prefix_id,
    )
    ref_record = ref_compute_metrics(
        reg_reference_dataset_abalone, reg_model_abalone, prefix_id
    )

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
        prefix_id,
    )
    ref_record = ref_compute_metrics(
        mc_reference_dataset_target_string, mc_model_target_string, prefix_id
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
        prefix_id,
    )
    ref_record = ref_compute_metrics(
        bc_reference_dataset_joined, bc_model_joined, prefix_id
    )

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
