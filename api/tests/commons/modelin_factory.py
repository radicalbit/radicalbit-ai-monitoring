from typing import List

from app.models.inferred_schema_dto import SupportedTypes
from app.models.model_dto import (
    ColumnDefinition,
    DataType,
    FieldType,
    Granularity,
    ModelType,
    OutputType,
)


def get_model_sample_wrong(fail_fields: List[str], model_type: ModelType):
    prediction = ColumnDefinition(
        name='pred1', type=SupportedTypes.int, field_type=FieldType.numerical
    )
    prediction_proba = ColumnDefinition(
        name='prob1', type=SupportedTypes.float, field_type=FieldType.numerical
    )
    target = ColumnDefinition(
        name='target1', type=SupportedTypes.int, field_type=FieldType.numerical
    )
    timestamp = ColumnDefinition(
        name='timestamp', type=SupportedTypes.datetime, field_type=FieldType.datetime
    )

    if 'outputs.prediction' in fail_fields:
        if model_type == ModelType.BINARY:
            prediction = ColumnDefinition(
                name='pred1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            )
        elif model_type == ModelType.MULTI_CLASS:
            prediction = ColumnDefinition(
                name='pred1',
                type=SupportedTypes.datetime,
                field_type=FieldType.datetime,
            )
        elif model_type == ModelType.REGRESSION:
            prediction = ColumnDefinition(
                name='pred1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            )

    if 'outputs.prediction_proba' in fail_fields:
        if model_type in (ModelType.BINARY, ModelType.MULTI_CLASS):
            prediction_proba = ColumnDefinition(
                name='prob1', type=SupportedTypes.int, field_type=FieldType.numerical
            )
        elif model_type == ModelType.REGRESSION:
            prediction_proba = ColumnDefinition(
                name='prob1', type=SupportedTypes.float, field_type=FieldType.numerical
            )

    if 'target' in fail_fields:
        if model_type == ModelType.BINARY:
            target = ColumnDefinition(
                name='target1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            )
        elif model_type == ModelType.MULTI_CLASS:
            target = ColumnDefinition(
                name='target1',
                type=SupportedTypes.datetime,
                field_type=FieldType.datetime,
            )
        elif model_type == ModelType.REGRESSION:
            target = ColumnDefinition(
                name='target1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            )

    if 'timestamp' in fail_fields:
        timestamp = ColumnDefinition(
            name='timestamp',
            type=SupportedTypes.string,
            field_type=FieldType.categorical,
        )

    return {
        'name': 'model_name',
        'model_type': model_type,
        'data_type': DataType.TEXT,
        'granularity': Granularity.DAY,
        'features': [
            ColumnDefinition(
                name='feature1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            )
        ],
        'outputs': OutputType(
            prediction=prediction,
            prediction_proba=prediction_proba,
            output=[
                ColumnDefinition(
                    name='output1',
                    type=SupportedTypes.string,
                    field_type=FieldType.categorical,
                )
            ],
        ),
        'target': target,
        'timestamp': timestamp,
        'frameworks': None,
        'algorithm': None,
    }
