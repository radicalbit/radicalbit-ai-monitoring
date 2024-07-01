from app.models.inferred_schema_dto import SupportedTypes
from app.models.model_dto import (
    ColumnDefinition,
    DataType,
    Granularity,
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
