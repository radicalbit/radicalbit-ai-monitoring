import datetime
from typing import Dict, List, Optional
import uuid

from app.db.tables.completion_dataset_metrics_table import CompletionDatasetMetrics
from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.model_table import Model
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.drift_algorithm_type import DriftAlgorithmType
from app.models.job_status import JobStatus
from app.models.model_dto import (
    ColumnDefinition,
    DataType,
    DriftMethod,
    FieldType,
    Granularity,
    ModelFeatures,
    ModelIn,
    ModelType,
    OutputType,
    SupportedTypes,
)

MODEL_UUID = uuid.uuid4()
REFERENCE_UUID = uuid.uuid4()
CURRENT_UUID = uuid.uuid4()
COMPLETION_UUID = uuid.uuid4()


def get_sample_model(
    id: int = 1,
    uuid: uuid.UUID = MODEL_UUID,
    name: str = 'model_name',
    description: Optional[str] = None,
    model_type: str = ModelType.BINARY.value,
    data_type: str = DataType.TEXT.value,
    granularity: str = Granularity.DAY.value,
    features: Optional[List[Dict]] = [
        {
            'name': 'feature1',
            'type': 'string',
            'fieldType': 'categorical',
            'drift': [{'name': 'CHI2', 'p_value': 0.4}],
        }
    ],
    outputs: Optional[Dict] = {
        'prediction': {'name': 'pred1', 'type': 'int', 'fieldType': 'numerical'},
        'prediction_proba': {
            'name': 'prob1',
            'type': 'float',
            'fieldType': 'numerical',
        },
        'output': [{'name': 'output1', 'type': 'string', 'fieldType': 'categorical'}],
    },
    target: Optional[Dict] = {
        'name': 'target1',
        'type': 'string',
        'fieldType': 'categorical',
    },
    timestamp: Optional[Dict] = {
        'name': 'timestamp',
        'type': 'datetime',
        'fieldType': 'datetime',
    },
    frameworks: Optional[str] = None,
    algorithm: Optional[str] = None,
) -> Model:
    return Model(
        id=id,
        uuid=uuid,
        name=name,
        description=description,
        model_type=model_type,
        data_type=data_type,
        granularity=granularity,
        features=features,
        outputs=outputs,
        target=target,
        timestamp=timestamp,
        frameworks=frameworks,
        algorithm=algorithm,
        created_at=datetime.datetime.now(tz=datetime.UTC),
        updated_at=datetime.datetime.now(tz=datetime.UTC),
    )


def get_sample_model_features(
    features: List[ColumnDefinition] = [
        ColumnDefinition(
            name='feature1',
            type=SupportedTypes.string,
            field_type=FieldType.categorical,
        )
    ],
):
    return ModelFeatures(features=features)


def get_sample_model_in(
    name: str = 'model_name',
    description: Optional[str] = None,
    model_type: str = ModelType.BINARY.value,
    data_type: str = DataType.TEXT.value,
    granularity: str = Granularity.DAY.value,
    features: Optional[List[ColumnDefinition]] = [
        ColumnDefinition(
            name='feature1',
            type=SupportedTypes.string,
            field_type=FieldType.categorical,
            drift=[DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.4)],
        )
    ],
    outputs: Optional[OutputType] = OutputType(
        prediction=ColumnDefinition(
            name='pred1', type=SupportedTypes.int, field_type=FieldType.numerical
        ),
        prediction_proba=ColumnDefinition(
            name='prob1', type=SupportedTypes.float, field_type=FieldType.numerical
        ),
        output=[
            ColumnDefinition(
                name='output1',
                type=SupportedTypes.string,
                field_type=FieldType.categorical,
            )
        ],
    ),
    target: Optional[ColumnDefinition] = ColumnDefinition(
        name='target1', type=SupportedTypes.int, field_type=FieldType.numerical
    ),
    timestamp: Optional[ColumnDefinition] = ColumnDefinition(
        name='timestamp', type=SupportedTypes.datetime, field_type=FieldType.datetime
    ),
    frameworks: Optional[str] = None,
    algorithm: Optional[str] = None,
):
    return ModelIn(
        name=name,
        description=description,
        model_type=model_type,
        data_type=data_type,
        granularity=granularity,
        features=features,
        outputs=outputs,
        target=target,
        timestamp=timestamp,
        frameworks=frameworks,
        algorithm=algorithm,
    )


def get_sample_reference_dataset(
    uuid: uuid.UUID = REFERENCE_UUID,
    model_uuid: uuid.UUID = MODEL_UUID,
    path: str = 'reference/test.csv',
    status: str = JobStatus.IMPORTING.value,
) -> ReferenceDataset:
    return ReferenceDataset(
        uuid=uuid,
        model_uuid=model_uuid,
        path=path,
        date=datetime.datetime.now(tz=datetime.UTC),
        status=status,
    )


def get_sample_current_dataset(
    uuid: uuid.UUID = CURRENT_UUID,
    model_uuid: uuid.UUID = MODEL_UUID,
    path: str = 'current/test.csv',
    status: str = JobStatus.IMPORTING.value,
) -> CurrentDataset:
    return CurrentDataset(
        uuid=uuid,
        model_uuid=model_uuid,
        path=path,
        date=datetime.datetime.now(tz=datetime.UTC),
        correlation_id_column='some_column',
        status=status,
    )


def get_sample_completion_dataset(
    uuid: uuid.UUID = COMPLETION_UUID,
    model_uuid: uuid.UUID = MODEL_UUID,
    path: str = 'completion/json_file.json',
    status: str = JobStatus.IMPORTING.value,
) -> CompletionDataset:
    return CompletionDataset(
        uuid=uuid,
        model_uuid=model_uuid,
        path=path,
        date=datetime.datetime.now(tz=datetime.UTC),
        status=status,
    )


statistics_dict = {
    'nVariables': 10,
    'nObservations': 1000,
    'missingCells': 50,
    'missingCellsPerc': 5.0,
    'duplicateRows': 10,
    'duplicateRowsPerc': 1.0,
    'numeric': 5,
    'categorical': 4,
    'datetime': 1,
}

model_quality_base_dict = {
    'f1': None,
    'accuracy': 0.90,
    'precision': 0.88,
    'recall': 0.87,
    'fMeasure': 0.85,
    'weightedPrecision': 0.88,
    'weightedRecall': 0.87,
    'weightedFMeasure': 0.85,
    'weightedTruePositiveRate': 0.90,
    'weightedFalsePositiveRate': 0.10,
    'truePositiveRate': 0.87,
    'falsePositiveRate': 0.13,
    'areaUnderRoc': 0.92,
    'areaUnderPr': 0.91,
    'logLoss': 0.71,
}

binary_model_quality_dict = {
    'truePositiveCount': 870,
    'falsePositiveCount': 130,
    'trueNegativeCount': 820,
    'falseNegativeCount': 180,
    **model_quality_base_dict,
}

grouped_metrics_dict = {
    'f1': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.8},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.85},
    ],
    'accuracy': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.88},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.9},
    ],
    'precision': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.86},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.88},
    ],
    'recall': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.81},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.83},
    ],
    'fMeasure': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.8},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.85},
    ],
    'weightedPrecision': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.85},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.87},
    ],
    'weightedRecall': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.82},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.84},
    ],
    'weightedFMeasure': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.84},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.86},
    ],
    'weightedTruePositiveRate': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.88},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.9},
    ],
    'weightedFalsePositiveRate': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.12},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.1},
    ],
    'truePositiveRate': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.81},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.83},
    ],
    'falsePositiveRate': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.14},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.12},
    ],
    'areaUnderRoc': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.94},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.95},
    ],
    'areaUnderPr': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.91},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.92},
    ],
    'logLoss': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.70},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.72},
    ],
}

binary_current_model_quality_dict = {
    'globalMetrics': binary_model_quality_dict,
    'groupedMetrics': grouped_metrics_dict,
}

multiclass_model_quality_dict = {
    'classes': [
        'classA',
        'classB',
        'classC',
    ],
    'class_metrics': [
        {
            'class_name': 'classA',
            'metrics': model_quality_base_dict,
            'grouped_metrics': grouped_metrics_dict,
        },
        {
            'class_name': 'classB',
            'metrics': model_quality_base_dict,
            'grouped_metrics': grouped_metrics_dict,
        },
        {
            'class_name': 'classC',
            'metrics': model_quality_base_dict,
            'grouped_metrics': grouped_metrics_dict,
        },
    ],
    'global_metrics': {
        'confusion_matrix': [
            [3.0, 0.0, 0.0, 0.0],
            [0.0, 2.0, 1.0, 0.0],
            [0.0, 0.0, 1.0, 2.0],
            [1.0, 0.0, 0.0, 0.0],
        ],
        **model_quality_base_dict,
    },
}

classification_data_quality_dict = {
    'nObservations': 200,
    'classMetrics': [
        {'name': 'classA', 'count': 100, 'percentage': 50.0},
        {'name': 'classB', 'count': 100, 'percentage': 50.0},
    ],
    'classMetricsPrediction': [
        {'name': 'classA', 'count': 100, 'percentage': 50.0},
        {'name': 'classB', 'count': 100, 'percentage': 50.0},
    ],
    'featureMetrics': [
        {
            'featureName': 'age',
            'type': 'numerical',
            'mean': 29.5,
            'std': 5.2,
            'min': 18,
            'max': 45,
            'medianMetrics': {'perc_25': 25.0, 'median': 29.0, 'perc_75': 34.0},
            'missingValue': {'count': 2, 'percentage': 0.02},
            'classMedianMetrics': [
                {
                    'name': 'classA',
                    'mean': 30.0,
                    'medianMetrics': {'perc_25': 27.0, 'median': 30.0, 'perc_75': 33.0},
                },
                {
                    'name': 'classB',
                    'mean': 29.0,
                    'medianMetrics': {'perc_25': 24.0, 'median': 28.0, 'perc_75': 32.0},
                },
            ],
            'histogram': {
                'buckets': [40.0, 45.0, 50.0, 55.0, 60.0],
                'referenceValues': [50, 150, 200, 150, 50],
                'currentValues': [45, 140, 210, 145, 60],
            },
        },
        {
            'featureName': 'gender',
            'type': 'categorical',
            'distinctValue': 2,
            'categoryFrequency': [
                {'name': 'male', 'count': 90, 'frequency': 0.45},
                {'name': 'female', 'count': 110, 'frequency': 0.55},
            ],
            'missingValue': {'count': 0, 'percentage': 0.0},
        },
    ],
}

regression_model_quality_dict = {
    'r2': 0.9131323648676931,
    'mae': 125.0137756497949,
    'mse': 40897.76059849524,
    'mape': 35.19314237273801,
    'rmse': 202.23194752188695,
    'adj_r2': 0.9116805380966796,
    'variance': 0.23,
    'residuals': {
        'ks': {
            'p_value': 0.01,
            'statistic': 0.4,
        },
        'histogram': {
            'values': [1, 2, 3],
            'buckets': [-3.2, -1, 2.2],
        },
        'correlation_coefficient': 0.01,
        'standardized_residuals': [0.02, 0.03],
        'targets': [1, 2.2, 3],
        'predictions': [1.3, 2, 4.5],
        'regression_line': {
            'coefficient': 0.7942363125434776,
            'intercept': 2.8227418911402906,
        },
    },
}

grouped_regression_model_quality_dict = {
    'r2': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.8},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.85},
    ],
    'mae': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.88},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.9},
    ],
    'mse': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.86},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.88},
    ],
    'mape': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.81},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.83},
    ],
    'rmse': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.8},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.85},
    ],
    'adj_r2': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.85},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.87},
    ],
    'variance': [
        {'timestamp': '2024-01-01T00:00:00Z', 'value': 0.82},
        {'timestamp': '2024-02-01T00:00:00Z', 'value': 0.84},
    ],
}

current_regression_model_quality_dict = {
    'global_metrics': regression_model_quality_dict,
    'grouped_metrics': grouped_regression_model_quality_dict,
}

regression_data_quality_dict = {
    'nObservations': 200,
    'targetMetrics': {
        'max': 3410.0,
        'min': 2.0,
        'std': 686.62,
        'mean': 848.12,
        'type': 'numerical',
        'histogram': {
            'buckets': [2.0, 342.8, 683.6, 1024.4],
            'reference_values': [204, 144, 165, 89],
        },
        'feature_name': 'ground_truth',
        'missing_value': {'count': 0, 'percentage': 0.0},
        'median_metrics': {'median': 713.0, 'perc_25': 315.0, 'perc_75': 1097.0},
    },
    'featureMetrics': [
        {
            'max': 731.0,
            'min': 1.0,
            'std': 211.16,
            'mean': 366.0,
            'type': 'numerical',
            'histogram': {
                'buckets': [1.0, 74.0, 147.0, 220.0],
                'reference_values': [73, 73, 73, 73],
            },
            'feature_name': 'instant',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'median_metrics': {'median': 366.0, 'perc_25': 183.5, 'perc_75': 548.5},
            'class_median_metrics': [],
        },
        {
            'max': 4.0,
            'min': 1.0,
            'std': 1.12,
            'mean': 2.49,
            'type': 'numerical',
            'histogram': {
                'buckets': [1.0, 1.3, 1.6, 1.9],
                'reference_values': [181, 0, 0, 184],
            },
            'feature_name': 'season',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'median_metrics': {'median': 3.0, 'perc_25': 2.0, 'perc_75': 3.0},
            'class_median_metrics': [],
        },
        {
            'type': 'categorical',
            'feature_name': 'Sex',
            'missing_value': {'count': 0, 'percentage': 0.0},
            'distinct_value': 3,
            'category_frequency': [
                {'name': 'F', 'count': 1064, 'frequency': 0.31837223219628963},
                {'name': 'M', 'count': 1208, 'frequency': 0.36146020347097546},
                {'name': 'I', 'count': 1070, 'frequency': 0.3201675643327349},
            ],
        },
    ],
}

drift_dict = {
    'featureMetrics': [
        {
            'featureName': 'gender',
            'fieldType': 'categorical',
            'driftCalc': [{'type': 'CHI2', 'value': 0.87, 'hasDrift': True}],
        },
        {
            'featureName': 'city',
            'fieldType': 'categorical',
            'driftCalc': [{'type': 'CHI2', 'value': 0.12, 'hasDrift': False}],
        },
        {
            'featureName': 'age',
            'fieldType': 'numerical',
            'driftCalc': [{'type': 'KS', 'value': 0.92, 'hasDrift': True}],
        },
    ]
}

percentages_dict = {
    'data_quality': {
        'value': 1.0,
        'details': [
            {'feature_name': 'num1', 'score': 0.0},
            {'feature_name': 'num2', 'score': 0.0},
            {'feature_name': 'cat1', 'score': 0.0},
            {'feature_name': 'cat2', 'score': 0.0},
        ],
    },
    'model_quality': {'value': -1, 'details': []},
    'drift': {
        'value': 0.5,
        'details': [
            {'feature_name': 'num1', 'score': 1.0},
            {'feature_name': 'num2', 'score': 1.0},
        ],
    },
}

model_quality_completion_dict = {
    'tokens': [
        {
            'id': 'chatcmpl',
            'message_content': 'Sky is blue.',
            'probs': [
                {'prob': 0.27718424797058105, 'token': 'Sky'},
                {'prob': 0.8951022028923035, 'token': ' is'},
                {'prob': 0.7038467526435852, 'token': ' blue'},
                {'prob': 0.9999753832817078, 'token': '.'},
            ],
            'rbit_timestamp': '2024-12-09 11:32:41',
            'total_token': 8,
            'model_name': 'gpt-4o-2024-08-06',
            'perplexity': 2.190884828567505,
            'probability': 0.6227279901504517,
        }
    ],
    'mean_per_file': [
        {'prob_tot_mean': 0.7190271615982056, 'perplex_tot_mean': 1.5469378232955933}
    ],
    'mean_per_phrase': [
        {
            'id': 'chatcmpl',
            'prob_per_phrase': 0.7190271615982056,
            'perplex_per_phrase': 1.5469378232955933,
        }
    ],
}


def get_sample_reference_metrics(
    reference_uuid: uuid.UUID = REFERENCE_UUID,
    model_quality: Dict = binary_model_quality_dict,
    data_quality: Dict = classification_data_quality_dict,
    statistics: Dict = statistics_dict,
) -> ReferenceDatasetMetrics:
    return ReferenceDatasetMetrics(
        reference_uuid=reference_uuid,
        model_quality=model_quality,
        statistics=statistics,
        data_quality=data_quality,
    )


def get_sample_current_metrics(
    current_uuid: uuid.UUID = CURRENT_UUID,
    model_quality: Dict = binary_current_model_quality_dict,
    data_quality: Dict = classification_data_quality_dict,
    statistics: Dict = statistics_dict,
    drift: Dict = drift_dict,
    percentages: Dict = percentages_dict,
) -> CurrentDatasetMetrics:
    return CurrentDatasetMetrics(
        current_uuid=current_uuid,
        model_quality=model_quality,
        statistics=statistics,
        data_quality=data_quality,
        drift=drift,
        percentages=percentages,
    )


def get_sample_completion_metrics(
    completion_uuid: uuid.UUID = COMPLETION_UUID,
    model_quality: Dict = model_quality_completion_dict,
) -> CompletionDatasetMetrics:
    return CompletionDatasetMetrics(
        completion_uuid=completion_uuid,
        model_quality=model_quality,
    )
