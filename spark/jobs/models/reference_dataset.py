from typing import List

from pyspark.ml.feature import StringIndexer
from pyspark.sql import DataFrame
from pyspark.sql.types import (
    DoubleType,
    StructField,
    StructType,
)
import pyspark.sql.functions as F
from pyspark.sql.window import Window

from utils.models import ModelOut, ModelType, ColumnDefinition
from utils.spark import apply_schema_to_dataframe


class ReferenceDataset:
    def __init__(self, model: ModelOut, raw_dataframe: DataFrame):
        reference_schema = self.spark_schema(model)
        reference_dataset = apply_schema_to_dataframe(raw_dataframe, reference_schema)

        self.model = model
        self.reference = reference_dataset.select(
            *[c for c in reference_schema.names if c in reference_dataset.columns]
        )
        self.reference_count = self.reference.count()

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

    def get_numerical_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_numerical()]

    def get_categorical_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_categorical()]

    def get_datetime_variables(self) -> List[ColumnDefinition]:
        all_features = (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )
        return [feature for feature in all_features if feature.is_datetime()]

    def get_all_variables(self) -> List[ColumnDefinition]:
        return (
            self.model.features
            + [self.model.target]
            + [self.model.timestamp]
            + self.model.outputs.output
        )

    def get_string_indexed_dataframe(self):
        """
        Source: https://stackoverflow.com/questions/65911146/how-to-transform-multiple-categorical-columns-to-integers-maintaining-shared-val
        """
        predictions_df = self.reference.select(
            self.model.outputs.prediction.name
        ).withColumnRenamed(self.model.outputs.prediction.name, "classes")
        target_df = self.reference.select(self.model.target.name).withColumnRenamed(
            self.model.target.name, "classes"
        )
        prediction_target_df = predictions_df.union(target_df).dropna()
        classes_index_df = prediction_target_df.select('classes').distinct() \
            .withColumn('classes_index', (F.row_number().over(Window.partitionBy(F.lit("A")).orderBy('classes')) - 1).cast(DoubleType()))
        indexed_prediction_df = self.reference.join(classes_index_df, self.reference[self.model.outputs.prediction.name]==classes_index_df["classes"], how="inner").withColumnRenamed('classes_index', f"{self.model.outputs.prediction.name}-idx").drop("classes")
        indexed_target_df = indexed_prediction_df.join(classes_index_df, indexed_prediction_df[self.model.target.name]==classes_index_df["classes"], how="inner").withColumnRenamed('classes_index', f"{self.model.target.name}-idx").drop("classes")

        index_label_map = {
            str(float(row.__getitem__('classes_index'))): str(row.__getitem__('classes'))
            for row in classes_index_df.collect()
        }
        return index_label_map, indexed_target_df
