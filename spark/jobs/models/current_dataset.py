from typing import List

from pyspark.sql import DataFrame
from pyspark.sql.types import DoubleType, StructField, StructType
import pyspark.sql.functions as F
from pyspark.sql.window import Window

from models.reference_dataset import ReferenceDataset
from utils.models import ModelOut, ModelType, ColumnDefinition
from utils.spark import apply_schema_to_dataframe


class CurrentDataset:
    def __init__(self, model: ModelOut, raw_dataframe: DataFrame, prefix_id: str):
        current_schema = self.spark_schema(model)
        current_dataset = apply_schema_to_dataframe(raw_dataframe, current_schema)

        self.model = model
        self.current = current_dataset.select(
            *[c for c in current_schema.names if c in current_dataset.columns]
        )
        self.current_count = self.current.count()
        self.prefix_id = prefix_id

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

    def get_float_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_float()]

    def get_int_features(self) -> List[ColumnDefinition]:
        return [feature for feature in self.model.features if feature.is_int()]

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

    def get_string_indexed_dataframe(self, reference: ReferenceDataset):
        """
        Source: https://stackoverflow.com/questions/65911146/how-to-transform-multiple-categorical-columns-to-integers-maintaining-shared-val
        Current dataset will be indexed with columns from both reference and current in order to have complete data
        """
        predictions_df_current = self.current.select(
            self.model.outputs.prediction.name
        ).withColumnRenamed(self.model.outputs.prediction.name, f"{self.prefix_id}_classes")
        target_df_current = self.current.select(
            self.model.target.name
        ).withColumnRenamed(self.model.target.name, f"{self.prefix_id}_classes")
        predictions_df_reference = reference.reference.select(
            self.model.outputs.prediction.name
        ).withColumnRenamed(self.model.outputs.prediction.name, f"{self.prefix_id}_classes")
        target_df_reference = reference.reference.select(
            self.model.target.name
        ).withColumnRenamed(self.model.target.name, f"{self.prefix_id}_classes")
        prediction_target_df = (
            predictions_df_current.union(target_df_current)
            .union(predictions_df_reference)
            .union(target_df_reference)
        ).dropna()
        classes_index_df = (
            prediction_target_df.select(f"{self.prefix_id}_classes")
            .distinct()
            .withColumn(
                f"{self.prefix_id}_classes_index",
                (
                    F.row_number().over(
                        Window.partitionBy(F.lit("A")).orderBy(f"{self.prefix_id}_classes")
                    )
                    - 1
                ).cast(DoubleType()),
            )
        )
        indexed_prediction_df = (
            self.current.join(
                classes_index_df,
                self.current[self.model.outputs.prediction.name]
                == classes_index_df[f"{self.prefix_id}_classes"],
                how="inner",
            )
            .withColumnRenamed(
                f"{self.prefix_id}_classes_index",
                f"{self.prefix_id}_{self.model.outputs.prediction.name}-idx",
            )
            .drop(f"{self.prefix_id}_classes")
        )
        indexed_target_df = (
            indexed_prediction_df.join(
                classes_index_df,
                indexed_prediction_df[self.model.target.name]
                == classes_index_df[f"{self.prefix_id}_classes"],
                how="inner",
            )
            .withColumnRenamed(
                f"{self.prefix_id}_classes_index", f"{self.prefix_id}_{self.model.target.name}-idx"
            )
            .drop(f"{self.prefix_id}_classes")
        )

        index_label_map = {
            str(float(row.__getitem__(f"{self.prefix_id}_classes_index"))): str(
                row.__getitem__(f"{self.prefix_id}_classes")
            )
            for row in classes_index_df.collect()
        }
        return index_label_map, indexed_target_df
