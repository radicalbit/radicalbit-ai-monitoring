from pydantic import ValidationError
import pytest

from app.models.inferred_schema_dto import SupportedTypes
from app.models.model_dto import (
    ColumnDefinition,
    DataType,
    Granularity,
    ModelIn,
    ModelType,
    OutputType,
)


def get_model_sample_wrong(fail_field: str, model_type: ModelType):
    prediction = None
    prediction_proba = None
    if fail_field == 'outputs.prediction' and model_type == ModelType.BINARY:
        prediction = ColumnDefinition(name='pred1', type=SupportedTypes.string)
    elif fail_field == 'outputs.prediction' and model_type == ModelType.MULTI_CLASS:
        prediction = ColumnDefinition(name='pred1', type=SupportedTypes.datetime)
    elif fail_field == 'outputs.prediction' and model_type == ModelType.REGRESSION:
        prediction = ColumnDefinition(name='pred1', type=SupportedTypes.string)
    else:
        prediction = ColumnDefinition(name='pred1', type=SupportedTypes.int)

    if (
        fail_field == 'outputs.prediction_proba'
        and model_type == ModelType.BINARY
        or fail_field == 'outputs.prediction_proba'
        and model_type == ModelType.MULTI_CLASS
    ):
        prediction_proba = ColumnDefinition(name='prob1', type=SupportedTypes.int)
    elif (
        fail_field == 'outputs.prediction_proba' and model_type == ModelType.REGRESSION
    ):
        prediction_proba = ColumnDefinition(name='prob1', type=SupportedTypes.float)
    else:
        prediction_proba = ColumnDefinition(name='prob1', type=SupportedTypes.float)

    target: ColumnDefinition = None
    if fail_field == 'target' and model_type == ModelType.BINARY:
        target = ColumnDefinition(name='target1', type=SupportedTypes.string)
    elif fail_field == 'target' and model_type == ModelType.MULTI_CLASS:
        target = ColumnDefinition(name='target1', type=SupportedTypes.datetime)
    elif fail_field == 'target' and model_type == ModelType.REGRESSION:
        target = ColumnDefinition(name='target1', type=SupportedTypes.string)
    else:
        target = ColumnDefinition(name='target1', type=SupportedTypes.int)

    timestamp: ColumnDefinition = None
    if fail_field == 'timestamp':
        timestamp = ColumnDefinition(name='timestamp', type=SupportedTypes.string)
    else:
        timestamp = ColumnDefinition(name='timestamp', type=SupportedTypes.datetime)

    return {
        'name': 'model_name',
        'model_type': model_type,
        'data_type': DataType.TEXT,
        'granularity': Granularity.DAY,
        'features': [ColumnDefinition(name='feature1', type=SupportedTypes.string)],
        'outputs': OutputType(
            prediction=prediction,
            prediction_proba=prediction_proba,
            output=[ColumnDefinition(name='output1', type=SupportedTypes.string)],
        ),
        'target': target,
        'timestamp': timestamp,
        'frameworks': None,
        'algorithm': None,
    }


def test_timestamp_not_datetime():
    """Tests that timestamp validator fails when timestamp is not valid."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            fail_field='timestamp', model_type=ModelType.BINARY
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'timestamp must be a datetime' in str(excinfo.value)


def test_target_for_binary():
    """Tests that for ModelType.BINARY: target must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong('target', ModelType.BINARY)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'target must be a number for a ModelType.BINARY' in str(excinfo.value)


def test_target_for_multiclass():
    """Tests that for ModelType.MULTI_CLASS: target must be a number or string."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong('target', ModelType.MULTI_CLASS)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'target must be a number or string for a ModelType.MULTI_CLASS' in str(
        excinfo.value
    )


def test_target_for_regression():
    """Tests that for ModelType.REGRESSION: target must be a number or string."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong('target', ModelType.REGRESSION)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'target must be a number for a ModelType.REGRESSION' in str(excinfo.value)


def test_prediction_for_binary():
    """Tests that for ModelType.BINARY: prediction must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong('outputs.prediction', ModelType.BINARY)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction must be a number for a ModelType.BINARY' in str(excinfo.value)


def test_prediction_for_multiclass():
    """Tests that for ModelType.MULTI_CLASS: prediction must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong('outputs.prediction', ModelType.MULTI_CLASS)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction must be a number or string for a ModelType.MULTI_CLASS' in str(
        excinfo.value
    )


def test_prediction_for_regression():
    """Tests that for ModelType.REGRESSION: prediction must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong('outputs.prediction', ModelType.REGRESSION)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction must be a number for a ModelType.REGRESSION' in str(
        excinfo.value
    )


def test_prediction_proba_for_binary():
    """Tests that for ModelType.BINARY: prediction_proba must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            'outputs.prediction_proba', ModelType.BINARY
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction_proba must be an optional float for a ModelType.BINARY' in str(
        excinfo.value
    )


def test_prediction_proba_for_multiclass():
    """Tests that for ModelType.MULTI_CLASS: prediction_proba must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            'outputs.prediction_proba', ModelType.MULTI_CLASS
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert (
        'prediction_proba must be an optional float for a ModelType.MULTI_CLASS'
        in str(excinfo.value)
    )


def test_prediction_proba_for_regression():
    """Tests that for ModelType.REGRESSION: prediction_proba must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            'outputs.prediction_proba', ModelType.REGRESSION
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction_proba must be None for a ModelType.REGRESSION' in str(
        excinfo.value
    )
