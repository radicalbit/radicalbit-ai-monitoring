from pydantic import ValidationError
import pytest

from app.models.drift_algorithm_type import DriftAlgorithmType
from app.models.inferred_schema_dto import FieldType, SupportedTypes
from app.models.metrics.drift_dto import FeatureMetrics
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


def test_validate_selection_drift_algorithms():
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


def test_set_default_feature_drift_algorithms_empty_list():
    model = db_mock.get_sample_model_in(
        model_type=ModelType.MULTI_CLASS,
        features=[
            ColumnDefinition(
                name='feature1',
                type=SupportedTypes.float,
                field_type=FieldType.numerical,
                drift=[],
            )
        ],
    )

    assert model.features[0].drift is None


def test_set_default_feature_drift_algorithms_none():
    model = db_mock.get_sample_model_in(
        model_type=ModelType.MULTI_CLASS,
        features=[
            ColumnDefinition(
                name='feature1',
                type=SupportedTypes.float,
                field_type=FieldType.numerical,
                drift=None,
            )
        ],
    )

    expected_drift_methods = [
        DriftMethod(name=DriftAlgorithmType.KS, p_value=0.05),
        DriftMethod(name=DriftAlgorithmType.WASSERSTEIN, threshold=0.1),
        DriftMethod(name=DriftAlgorithmType.PSI, threshold=0.1),
        DriftMethod(name=DriftAlgorithmType.HELLINGER, threshold=0.1),
        DriftMethod(name=DriftAlgorithmType.JS, threshold=0.1),
        DriftMethod(name=DriftAlgorithmType.KL, threshold=0.1),
    ]

    assert model.features[0].drift == expected_drift_methods


def test_set_specific_feature_drift_algorithms():
    drift_methods = [
        DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05),
        DriftMethod(name=DriftAlgorithmType.KL, threshold=0.1),
    ]
    model = db_mock.get_sample_model_in(
        model_type=ModelType.MULTI_CLASS,
        features=[
            ColumnDefinition(
                name='feature1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
                drift=drift_methods,
            )
        ],
    )

    assert model.features[0].drift == drift_methods


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


def test_validate_old_drift():
    input_dict = {
        'drift_calc': {
            'type': 'HELLINGER',
            'value': 0.7099295739719539,
            'has_drift': True,
            'limit': 0.1,
        },
        'field_type': 'categorical',
        'feature_name': 'user_id',
    }
    assert FeatureMetrics.model_validate(input_dict)
