from collections import namedtuple
import datetime
from typing import Dict, List, Optional
import uuid

from app.db.tables.api_key_table import ApiKey
from app.db.tables.completion_dataset_metrics_table import CompletionDatasetMetrics
from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.model_table import Model
from app.db.tables.project_table import Project
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.db.tables.traces_table import Trace
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
from app.models.traces.api_key_dto import ApiKeyIn, ApiKeySec
from app.models.traces.project_dto import ProjectIn

MODEL_UUID = uuid.uuid4()
REFERENCE_UUID = uuid.uuid4()
CURRENT_UUID = uuid.uuid4()
COMPLETION_UUID = uuid.uuid4()
PROJECT_UUID = uuid.uuid4()
SESSION_UUID = uuid.uuid4()
TRACE_ID = str(uuid.uuid4())
SPAN_ID = str(uuid.uuid4())
HASHED_KEY = 'da4af9c445b9bc1686ba63455d7c34aa569aeb09b95f395963dc7777a2afc6d4'
PLAIN_KEY = 'sk-rb-SmnyH9HPJfwyRpJ2vfZEO0ugFWykvwarbEQ2PPpTezpsueV1'
OBSCURED_KEY = 'sk-rb-Sm...eV1'


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
            'driftCalc': [
                {'type': 'CHI2', 'value': 0.87, 'hasDrift': True, 'limit': 0.05}
            ],
        },
        {
            'featureName': 'city',
            'fieldType': 'categorical',
            'driftCalc': [
                {'type': 'CHI2', 'value': 0.12, 'hasDrift': False, 'limit': 0.05}
            ],
        },
        {
            'featureName': 'age',
            'fieldType': 'numerical',
            'driftCalc': [
                {'type': 'KS', 'value': 0.92, 'hasDrift': True, 'limit': 0.1}
            ],
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


def get_sample_api_key(
    name: str = 'default',
    project_uuid: PROJECT_UUID = PROJECT_UUID,
    hashed_key: str = HASHED_KEY,
    obscured_key: str = OBSCURED_KEY,
) -> ApiKey:
    now = datetime.datetime.now(tz=datetime.UTC)
    return ApiKey(
        name=name,
        project_uuid=project_uuid,
        hashed_key=hashed_key,
        obscured_key=obscured_key,
        created_at=now,
        updated_at=now,
    )


def get_sample_api_key_sec(
    plain_key: str = PLAIN_KEY, hashed_key: str = HASHED_KEY
) -> ApiKeySec:
    return ApiKeySec(plain_key=plain_key, hashed_key=hashed_key)


def get_sample_api_key_in(name: str = 'api_key') -> ApiKeyIn:
    return ApiKeyIn(name=name)


def get_sample_project(
    uuid: uuid.UUID = PROJECT_UUID, name: str = 'project_name'
) -> Project:
    now = datetime.datetime.now(tz=datetime.UTC)
    return Project(
        uuid=uuid,
        name=name,
        created_at=now,
        updated_at=now,
        api_keys=[get_sample_api_key()],
    )


def get_sample_project_in(
    name: str = 'project_name',
):
    return ProjectIn(
        name=name,
    )


def get_sample_trace(
    session_uuid: uuid.UUID = SESSION_UUID,
    trace_id: str = TRACE_ID,
    span_id: str = SPAN_ID,
    project_uuid: uuid.UUID = PROJECT_UUID,
    completion_tokens: int = 100,
    prompt_tokens: int = 100,
    timestamp: datetime = datetime.datetime.now(tz=datetime.UTC),
    duration: int = 1194567000,
) -> Trace:
    return Trace(
        timestamp=timestamp,
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id='',
        trace_state='',
        span_name='ChatOpenAI.chat',
        span_kind='Client',
        service_name=str(project_uuid),
        resource_attributes={
            'env': 'dev',
            'service.name': 'test',
            'test': 'lalalal',
            'version': '1.0.0',
        },
        scope_name='opentelemetry.instrumentation.langchain',
        scope_version='0.38.12',
        span_attributes={
            'gen_ai.completion.0.content': 'Action: list_tables_sql_db\nAction Input: ',
            'gen_ai.completion.0.role': 'assistant',
            'gen_ai.prompt.0.content': 'You are an agent designed to interact with Spark SQL.\nGiven an input question, create a syntactically correct Spark SQL query to run, then look at the results of the query and return the answer.\nUnless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 10 results.\nYou can order the results by a relevant column to return the most interesting examples in the database.\nNever query for all the columns from a specific table, only ask for the relevant columns given the question.\nYou have access to tools for interacting with the database.\nOnly use the below tools. Only use the information returned by the below tools to construct your final answer.\nYou MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.\n\nDO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.\n\nIf the question does not seem related to the database, just return "I don\'t know" as the answer.\n\n\nquery_sql_db - \n    Input to this tool is a detailed and correct SQL query, output is a result from the Spark SQL.\n    If the query is not correct, an error message will be returned.\n    If an error is returned, rewrite the query, check the query, and try again.\n    \nschema_sql_db - \n    Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.\n    Be sure that the tables actually exist by calling list_tables_sql_db first!\n\n    Example Input: "table1, table2, table3"\n    \nlist_tables_sql_db - Input is an empty string, output is a comma separated list of tables in the Spark SQL.\nquery_checker_sql_db - \n    Use this tool to double check if your query is correct before executing it.\n    Always use this tool before executing a query with query_sql_db!\n    \n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [query_sql_db, schema_sql_db, list_tables_sql_db, query_checker_sql_db]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: mean of ages\nThought: I should look at the tables in the database to see what I can query.\n',
            'gen_ai.prompt.0.role': 'user',
            'gen_ai.request.model': 'gpt-3.5-turbo',
            'gen_ai.request.temperature': '0',
            'gen_ai.response.model': 'gpt-3.5-turbo-0125',
            'gen_ai.system': 'Langchain',
            'gen_ai.usage.completion_tokens': f'{completion_tokens}',
            'gen_ai.usage.prompt_tokens': f'{prompt_tokens}',
            'llm.request.type': 'chat',
            'llm.usage.total_tokens': f'{sum((completion_tokens, prompt_tokens))}',
            'traceloop.association.properties.ls_model_name': 'gpt-3.5-turbo',
            'traceloop.association.properties.ls_model_type': 'chat',
            'traceloop.association.properties.ls_provider': 'openai',
            'traceloop.association.properties.ls_stop': '["\\nObservation:","\\n\\tObservation:"]',
            'traceloop.association.properties.ls_temperature': '0',
            'traceloop.association.properties.session_uuid': str(session_uuid),
            'traceloop.entity.path': 'LLMChain',
            'traceloop.workflow.name': 'AgentExecutor',
        },
        duration=duration,
        status_code='Unset',
        status_message='',
        events=[],
        links=[],
    )


def get_sample_trace_tree(
    session_uuid: uuid.UUID = SESSION_UUID,
    trace_id: str = TRACE_ID,
    span_id: str = SPAN_ID,
    parent_span_id: str = '',
    span_name: str = 'ChannelWrite<...,action>.task',
    project_uuid: uuid.UUID = PROJECT_UUID,
    timestamp: datetime = datetime.datetime.now(tz=datetime.UTC),
    duration: int = 808036,
) -> Trace:
    return Trace(
        timestamp=timestamp,
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        trace_state='',
        span_name=span_name,
        span_kind='Internal',
        service_name=str(project_uuid),
        resource_attributes={},
        scope_name='opentelemetry.instrumentation.langchain',
        scope_version='0.38.12',
        span_attributes={
            'traceloop.association.properties.langgraph_checkpoint_ns': 'action:c6f1c3fb-c537-7bb7-fec1-d5b2cb87b57c',
            'traceloop.association.properties.langgraph_node': 'action',
            'traceloop.association.properties.langgraph_path': '["__pregel_pull","action"]',
            'traceloop.association.properties.langgraph_step': '4',
            'traceloop.association.properties.langgraph_triggers': '["branch:agent:should_continue:action"]',
            'traceloop.association.properties.session_uuid': str(session_uuid),
            'traceloop.entity.input': '{"inputs": {"messages": [{"lc": 1, "type": "constructor", "id": ["langchain", "schema", "messages", "ToolMessage"], "kwargs": {"content": "Page: Steve Jobs\\nSummary: Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, inventor, and investor best known for co-founding the technology company Apple Inc. Jobs was also the founder of NeXT and chairman and majority shareholder of Pixar. He was a pioneer of the personal computer revolution of the 1970s and 1980s, along with his early business partner and fellow Apple co-founder Steve Wozniak.\\nJobs was born in San Francisco in 1955 and adopted shortly afterwards. He attended Reed College in 1972 before withdrawing that same year. In 1974, he traveled through India, seeking enlightenment before later studying Zen Buddhism. He and Wozniak co-founded Apple in 1976 to further develop and sell Wozniak\'s Apple I personal computer. Together, the duo gained fame and wealth a year later with production and sale of the Apple II, one of the first highly successful mass-produced microcomputers. \\nJobs saw the commercial potential of the Xerox Alto in 1979, which was mouse-driven and had a graphical user interface (GUI). This led to the development of the largely unsuccessful Apple Lisa in 1983, followed by the breakthrough Macintosh in 1984, the first mass-produced computer with a GUI. The Macintosh launched the desktop publishing industry in 1985 (for example, the Aldus Pagemaker) with the addition of the Apple LaserWriter, the first laser printer to feature vector graphics and PostScript.\\nIn 1985, Jobs departed Apple after a long power struggle with the company\'s board and its then-CEO, John Sculley. That same year, Jobs took some Apple employees with him to found NeXT, a computer platform development company that specialized in computers for higher-education and business markets, serving as its CEO. In 1986, he bought the computer graphics division of Lucasfilm, which was spun off independently as Pixar. Pixar produced the first computer-animated feature film, Toy Story (1995), and became a leading animation studio, producing dozens of commercially successful and critically acclaimed films.\\nIn 1997, Jobs returned to Apple as CEO after the company\'s acquisition of NeXT. He was largely responsible for reviving Apple, which was on the verge of bankruptcy. He worked closely with British designer Jony Ive to develop a line of products and services that had larger cultural ramifications, beginning with the \\"Think different\\" advertising campaign, and leading to the iMac, iTunes, Mac OS X, Apple Store, iPod, iTunes Store, iPhone, App Store, and iPad. Jobs was also a board member at Gap Inc. from 1999 to 2002. In 2003, Jobs was diagnosed with a pancreatic neuroendocrine tumor. He died of tumor-related respiratory arrest in 2011; in 2022, he was posthumously awarded the Presidential Medal of Freedom. Since his death, he has won 141 patents; Jobs holds over 450 patents in total.\\n\\nPage: Steve Jobs (film)\\nSummary: Steve Jobs is a 2015 biographical drama film directed by Danny Boyle and written by Aaron Sorkin. A British-American co-production, it was adapted from the 2011 biography by Walter Isaacson and interviews conducted by Sorkin. The film covers fourteen years in the life of Apple Inc. co-founder Steve Jobs, specifically ahead of three press conferences he gave during that time: the formal unveiling of the Macintosh 128K on January 24, 1984; the unveiling of the NeXT Computer on October 12, 1988; and the unveiling of the iMac G3 on May 6, 1998. Jobs is portrayed by Michael Fassbender, with Kate Winslet as Joanna Hoffman, Seth Rogen as Steve Wozniak, and Jeff Daniels as John Sculley in supporting roles.\\nDevelopment began in 2011 after the rights to Isaacson\'s book were acquired. Filming began in January 2015. A variety of actors were considered and cast before Fassbender eventually took the role. Editing was extensive on the project, with editor Elliot Graham starting while the film was still shooting. Daniel Pemberton served as composer, with a focus on dividing the score into three distinguishable sections", "type": "tool", "name": "wikipedia", "tool_call_id": "call_N74miCWuGpUVMaaeLpHnDuSg", "status": "success"}}]}, "tags": ["seq:step:2", "langsmith:hidden"], "metadata": {"thread_id": "00000000-0000-0000-0000-000000000092", "langgraph_step": 4, "langgraph_node": "action", "langgraph_triggers": ["branch:agent:should_continue:action"], "langgraph_path": ["__pregel_pull", "action"], "langgraph_checkpoint_ns": "action:c6f1c3fb-c537-7bb7-fec1-d5b2cb87b57c"}, "kwargs": {"name": "ChannelWrite<...,action>"}}',
            'traceloop.entity.name': 'ChannelWrite<...,action>',
            'traceloop.entity.output': '{"outputs": {"messages": [{"lc": 1, "type": "constructor", "id": ["langchain", "schema", "messages", "ToolMessage"], "kwargs": {"content": "Page: Steve Jobs\\nSummary: Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, inventor, and investor best known for co-founding the technology company Apple Inc. Jobs was also the founder of NeXT and chairman and majority shareholder of Pixar. He was a pioneer of the personal computer revolution of the 1970s and 1980s, along with his early business partner and fellow Apple co-founder Steve Wozniak.\\nJobs was born in San Francisco in 1955 and adopted shortly afterwards. He attended Reed College in 1972 before withdrawing that same year. In 1974, he traveled through India, seeking enlightenment before later studying Zen Buddhism. He and Wozniak co-founded Apple in 1976 to further develop and sell Wozniak\'s Apple I personal computer. Together, the duo gained fame and wealth a year later with production and sale of the Apple II, one of the first highly successful mass-produced microcomputers. \\nJobs saw the commercial potential of the Xerox Alto in 1979, which was mouse-driven and had a graphical user interface (GUI). This led to the development of the largely unsuccessful Apple Lisa in 1983, followed by the breakthrough Macintosh in 1984, the first mass-produced computer with a GUI. The Macintosh launched the desktop publishing industry in 1985 (for example, the Aldus Pagemaker) with the addition of the Apple LaserWriter, the first laser printer to feature vector graphics and PostScript.\\nIn 1985, Jobs departed Apple after a long power struggle with the company\'s board and its then-CEO, John Sculley. That same year, Jobs took some Apple employees with him to found NeXT, a computer platform development company that specialized in computers for higher-education and business markets, serving as its CEO. In 1986, he bought the computer graphics division of Lucasfilm, which was spun off independently as Pixar. Pixar produced the first computer-animated feature film, Toy Story (1995), and became a leading animation studio, producing dozens of commercially successful and critically acclaimed films.\\nIn 1997, Jobs returned to Apple as CEO after the company\'s acquisition of NeXT. He was largely responsible for reviving Apple, which was on the verge of bankruptcy. He worked closely with British designer Jony Ive to develop a line of products and services that had larger cultural ramifications, beginning with the \\"Think different\\" advertising campaign, and leading to the iMac, iTunes, Mac OS X, Apple Store, iPod, iTunes Store, iPhone, App Store, and iPad. Jobs was also a board member at Gap Inc. from 1999 to 2002. In 2003, Jobs was diagnosed with a pancreatic neuroendocrine tumor. He died of tumor-related respiratory arrest in 2011; in 2022, he was posthumously awarded the Presidential Medal of Freedom. Since his death, he has won 141 patents; Jobs holds over 450 patents in total.\\n\\nPage: Steve Jobs (film)\\nSummary: Steve Jobs is a 2015 biographical drama film directed by Danny Boyle and written by Aaron Sorkin. A British-American co-production, it was adapted from the 2011 biography by Walter Isaacson and interviews conducted by Sorkin. The film covers fourteen years in the life of Apple Inc. co-founder Steve Jobs, specifically ahead of three press conferences he gave during that time: the formal unveiling of the Macintosh 128K on January 24, 1984; the unveiling of the NeXT Computer on October 12, 1988; and the unveiling of the iMac G3 on May 6, 1998. Jobs is portrayed by Michael Fassbender, with Kate Winslet as Joanna Hoffman, Seth Rogen as Steve Wozniak, and Jeff Daniels as John Sculley in supporting roles.\\nDevelopment began in 2011 after the rights to Isaacson\'s book were acquired. Filming began in January 2015. A variety of actors were considered and cast before Fassbender eventually took the role. Editing was extensive on the project, with editor Elliot Graham starting while the film was still shooting. Daniel Pemberton served as composer, with a focus on dividing the score into three distinguishable sections", "type": "tool", "name": "wikipedia", "tool_call_id": "call_N74miCWuGpUVMaaeLpHnDuSg", "status": "success"}}]}, "kwargs": {"tags": ["seq:step:2", "langsmith:hidden"]}}',
            'traceloop.entity.path': 'action',
            'traceloop.span.kind': 'task',
            'traceloop.workflow.name': 'LangGraph',
            'gen_ai.usage.completion_tokens': '10',
            'gen_ai.usage.prompt_tokens': '500',
            'llm.request.type': 'chat',
            'llm.usage.total_tokens': '510',
        },
        duration=duration,
        status_code='Unset',
        status_message='',
        events=[],
        links=[],
    )


def get_sample_session_tuple():
    Row = namedtuple(
        'Row',
        [
            'project_uuid',
            'session_uuid',
            'created_at',
            'latest_trace_ts',
            'traces',
            'duration',
            'no_label',
            'completion_tokens',
            'prompt_tokens',
            'total_tokens',
            'session_uuid_1',
            'number_of_errors',
        ],
    )
    d = [
        (
            '00000000-0000-0000-0000-000000000000',
            '286751f8-398c-4a8c-898f-78caf9453fde',
            '2025-03-17 13:14:56.706105000',
            '2025-03-17 13:14:56.706209000',
            2,
            1355537000,
            '286751f8-398c-4a8c-898f-78caf9453fde',
            62,
            1669,
            1731,
            '286751f8-398c-4a8c-898f-78caf9453fde',
            0,
        ),
        (
            '00000000-0000-0000-0000-000000000000',
            'a8dd1f4d-d076-4035-99e2-443c550c71a4',
            '2025-03-17 13:14:56.701422000',
            '2025-03-17 13:14:56.705982000',
            2,
            1780675000,
            'a8dd1f4d-d076-4035-99e2-443c550c71a4',
            36,
            1091,
            1127,
            'a8dd1f4d-d076-4035-99e2-443c550c71a4',
            0,
        ),
    ]
    return [Row(*item) for item in d]


def get_sample_trace_roots():
    Row = namedtuple(
        'Row',
        [
            'project_uuid',
            'session_uuid',
            'trace_id',
            'span_id',
            'spans',
            'created_at',
            'latest_span_ts',
            'duration',
            'completion_tokens',
            'prompt_tokens',
            'total_tokens',
            'number_of_errors',
        ],
    )
    d = [
        (
            '00000000-0000-0000-0000-000000000000',
            '286751f8-398c-4a8c-898f-78caf9453fde',
            'trace-1',
            'span-153463652',
            5,
            '2025-03-17 13:14:56.706105000',
            '2025-03-17 13:14:56.706209000',
            1355537000,
            62,
            1669,
            1731,
            0,
        ),
        (
            '00000000-0000-0000-0000-000000000000',
            '286751f8-398c-4a8c-898f-78caf9453fdd',
            'trace-2',
            'span-12345',
            10,
            '2025-03-18 13:14:56.706105000',
            '2025-03-18 13:14:56.706209000',
            355537000,
            60,
            500,
            560,
            0,
        ),
        (
            '00000000-0000-0000-0000-000000000000',
            '286751f8-398c-4a8c-898f-78caf9453fdd',
            'trace-2',
            'span-63453453',
            3,
            '2025-03-19 13:14:56.706105000',
            '2025-03-19 13:14:56.706209000',
            500000000,
            1,
            10,
            11,
            2,
        ),
    ]
    return [Row(*item) for item in d]


def get_sample_dao_trace_time():
    return [
        {'count': 1, 'start_date': datetime.datetime(2025, 3, 17, 9, 37, 0, 0)},
        {'count': 7, 'start_date': datetime.datetime(2025, 3, 19, 12, 13, 0, 0)},
    ]


def get_sample_trace_by_session(session_uuid: str, count: int) -> dict:
    return {'session_uuid': session_uuid, 'count': count}
