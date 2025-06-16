import unittest

from pydantic import ValidationError
import pytest

from app.models.drift_algorithm_type import DriftAlgorithmType
from app.models.inferred_schema_dto import FieldType, SupportedTypes
from app.models.model_dto import (
    ColumnDefinition,
    ColumnDefinitionFE,
    DriftMethod,
    ModelFeatures,
    ModelFeaturesFE,
)


class ModelDTOTest(unittest.TestCase):
    def test_model_features_default(self):
        column = ColumnDefinitionFE(
            name='test', type=SupportedTypes.string, field_type=FieldType.categorical
        )
        model_feature_fe = ModelFeaturesFE(features=[column])
        model_feature_default = model_feature_fe.to_model_features_default()
        assert model_feature_default == ModelFeatures(
            features=[
                ColumnDefinition(
                    name='test',
                    type=SupportedTypes.string,
                    field_type=FieldType.categorical,
                    drift=[
                        DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05),
                        DriftMethod(name=DriftAlgorithmType.JS, threshold=0.1),
                        DriftMethod(name=DriftAlgorithmType.KL, threshold=0.1),
                        DriftMethod(name=DriftAlgorithmType.HELLINGER, threshold=0.1),
                    ],
                )
            ]
        )

    def test_model_features_default_fail_if_incompatible(self):
        column = ColumnDefinitionFE(
            name='test', type=SupportedTypes.string, field_type=FieldType.numerical
        )
        model_feature_fe = ModelFeaturesFE(features=[column])
        with pytest.raises(ValidationError):
            model_feature_fe.to_model_features_default()
