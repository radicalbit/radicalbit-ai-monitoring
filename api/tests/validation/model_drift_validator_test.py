from pydantic import ValidationError
import pytest

from app.models.drift_algorithm_type import DriftAlgorithmType
from app.models.inferred_schema_dto import FieldType, SupportedTypes
from app.models.model_dto import ColumnDefinition, DriftMethod, ModelType
from tests.commons import db_mock


def test_validate_drift_scope():
    with pytest.raises(ValidationError) as excinfo:
        db_mock.get_sample_model_in(
            model_type=ModelType.MULTI_CLASS,
            features=[
                ColumnDefinition(
                    name='feature1',
                    type=SupportedTypes.string,
                    field_type=FieldType.categorical,
                    drift=[DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05)],
                )
            ],
            target=ColumnDefinition(
                name='target',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
                drift=[DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05)],
            ),
        )
    assert 'Drift can only be enabled on the features field' in str(excinfo.value)


def test_validate_drift_algorithm_type():
    with pytest.raises(ValidationError) as excinfo:
        db_mock.get_sample_model_in(
            model_type=ModelType.MULTI_CLASS,
            features=[
                ColumnDefinition(
                    name='feature1',
                    type=SupportedTypes.float,
                    field_type=FieldType.numerical,
                    drift=[DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05)],
                )
            ],
        )

    assert (
        f'{DriftAlgorithmType.CHI2.value} can only be used with categorical fields'
        in str(excinfo.value)
    )


def test_validate_drift_threshold_requirement():
    with pytest.raises(ValidationError) as excinfo:
        db_mock.get_sample_model_in(
            model_type=ModelType.MULTI_CLASS,
            features=[
                ColumnDefinition(
                    name='feature1',
                    type=SupportedTypes.float,
                    field_type=FieldType.numerical,
                    drift=[DriftMethod(name=DriftAlgorithmType.HELLINGER)],
                )
            ],
        )

    assert f'{DriftAlgorithmType.HELLINGER.value} requires a threshold' in str(
        excinfo.value
    )


def test_validate_drift_p_value_requirement():
    with pytest.raises(ValidationError) as excinfo:
        db_mock.get_sample_model_in(
            model_type=ModelType.MULTI_CLASS,
            features=[
                ColumnDefinition(
                    name='feature1',
                    type=SupportedTypes.string,
                    field_type=FieldType.categorical,
                    drift=[DriftMethod(name=DriftAlgorithmType.CHI2)],
                )
            ],
        )

    assert f'{DriftAlgorithmType.CHI2.value} requires a p_value' in str(excinfo.value)
