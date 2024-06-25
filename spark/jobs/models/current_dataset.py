from typing import List

from pyspark.sql import DataFrame
from pyspark.sql.types import DoubleType, StructField, StructType

from ..utils.models import ModelOut, ModelType, ColumnDefinition
from ..utils.spark import apply_schema_to_dataframe


class CurrentDataset:
    def __init__(self, model: ModelOut, raw_dataframe: DataFrame):
        current_schema = self.spark_schema(model)
        current_dataset = apply_schema_to_dataframe(raw_dataframe, current_schema)

        self.model = model
        self.current = current_dataset.select(
            *[c for c in current_schema.names if c in current_dataset.columns]
        )
        self.current_count = self.current.count()

    # FIXME this must exclude target when we will have separate current and ground truth
    @staticmethod
    def spark_schema(model: ModelOut):
        all_features = (
            model.features + [model.target] + [model.timestamp] + model.outputs.output
        )
        if model.outputs.prediction_proba and model.model_type == ModelType.BINARY:
            enforce_float = [
                model.target.name,
                model.outputs.prediction.name,
                model.outputs.prediction_proba.name,
            ]
        elif model.model_type == ModelType.BINARY:
            enforce_float = [model.target.name, model.outputs.prediction.name]
        else:
            enforce_float = []
        return StructType(
            [
                StructField(
                    name=feature.name,
                    dataType=model.convert_types(feature.type),
                    nullable=False,
                )
                if feature.name not in enforce_float
                else StructField(
                    name=feature.name,
                    dataType=DoubleType(),
                    nullable=False,
                )
                for feature in all_features
            ]
        )

    def get_numerical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_numerical()]

    def get_categorical_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_categorical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_numerical_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_numerical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_categorical_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_categorical()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_datetime_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_datetime()]

    # FIXME this must exclude target when we will have separate current and ground truth
    def get_all_variables(self) -> List[ColumnDefinition]:
        return (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
