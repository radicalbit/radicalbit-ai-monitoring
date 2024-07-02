from pydantic import ValidationError
import pytest

from app.models.model_dto import ModelIn, ModelType
from tests.commons.modelin_factory import get_model_sample_wrong


def test_timestamp_not_datetime():
    """Tests that timestamp validator fails when timestamp is not valid."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            fail_fields=['timestamp'], model_type=ModelType.BINARY
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'timestamp must be a datetime' in str(excinfo.value)


def test_target_for_binary():
    """Tests that for ModelType.BINARY: target must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(['target'], ModelType.BINARY)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'target must be a number for a ModelType.BINARY' in str(excinfo.value)


def test_target_for_multiclass():
    """Tests that for ModelType.MULTI_CLASS: target must be a number or string."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(['target'], ModelType.MULTI_CLASS)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'target must be a number or string for a ModelType.MULTI_CLASS' in str(
        excinfo.value
    )


def test_target_for_regression():
    """Tests that for ModelType.REGRESSION: target must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(['target'], ModelType.REGRESSION)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'target must be a number for a ModelType.REGRESSION' in str(excinfo.value)


def test_prediction_for_binary():
    """Tests that for ModelType.BINARY: prediction must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(['outputs.prediction'], ModelType.BINARY)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction must be a number for a ModelType.BINARY' in str(excinfo.value)


def test_prediction_for_multiclass():
    """Tests that for ModelType.MULTI_CLASS: prediction must be a number or string."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(['outputs.prediction'], ModelType.MULTI_CLASS)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction must be a number or string for a ModelType.MULTI_CLASS' in str(
        excinfo.value
    )


def test_prediction_for_regression():
    """Tests that for ModelType.REGRESSION: prediction must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(['outputs.prediction'], ModelType.REGRESSION)
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction must be a number for a ModelType.REGRESSION' in str(
        excinfo.value
    )


def test_prediction_proba_for_binary():
    """Tests that for ModelType.BINARY: prediction_proba must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            ['outputs.prediction_proba'], ModelType.BINARY
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction_proba must be an optional float for a ModelType.BINARY' in str(
        excinfo.value
    )


def test_prediction_proba_for_multiclass():
    """Tests that for ModelType.MULTI_CLASS: prediction_proba must be a number."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            ['outputs.prediction_proba'], ModelType.MULTI_CLASS
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert (
        'prediction_proba must be an optional float for a ModelType.MULTI_CLASS'
        in str(excinfo.value)
    )


def test_prediction_proba_for_regression():
    """Tests that for ModelType.REGRESSION: prediction_proba must be None."""
    with pytest.raises(ValidationError) as excinfo:
        model_data = get_model_sample_wrong(
            ['outputs.prediction_proba'], ModelType.REGRESSION
        )
        ModelIn.model_validate(ModelIn(**model_data))
    assert 'prediction_proba must be None for a ModelType.REGRESSION' in str(
        excinfo.value
    )
