import datetime
from typing import Dict, List, Optional
import uuid

from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.model_table import Model
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.job_status import JobStatus
from app.models.model_dto import DataType, Granularity, ModelIn, ModelType

MODEL_UUID = uuid.uuid4()
REFERENCE_UUID = uuid.uuid4()
CURRENT_UUID = uuid.uuid4()


def get_sample_model(
    id: int = 1,
    uuid: uuid.UUID = MODEL_UUID,
    name: str = 'model_name',
    description: Optional[str] = None,
    model_type: str = ModelType.BINARY.value,
    data_type: str = DataType.TEXT.value,
    granularity: str = Granularity.DAY.value,
    features: List[Dict] = [{'name': 'feature1', 'type': 'string'}],
    outputs: Dict = {
        'prediction': {'name': 'pred1', 'type': 'int'},
        'prediction_proba': {'name': 'prob1', 'type': 'double'},
        'output': [{'name': 'output1', 'type': 'string'}],
    },
    target: Dict = {'name': 'target1', 'type': 'string'},
    timestamp: Dict = {'name': 'timestamp', 'type': 'datetime'},
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


def get_sample_model_in(
    name: str = 'model_name',
    description: Optional[str] = None,
    model_type: str = ModelType.BINARY.value,
    data_type: str = DataType.TEXT.value,
    granularity: str = Granularity.DAY.value,
    features: List[Dict] = [{'name': 'feature1', 'type': 'string'}],
    outputs: Dict = {
        'prediction': {'name': 'pred1', 'type': 'int'},
        'prediction_proba': {'name': 'prob1', 'type': 'double'},
        'output': [{'name': 'output1', 'type': 'string'}],
    },
    target: Dict = {'name': 'target1', 'type': 'string'},
    timestamp: Dict = {'name': 'timestamp', 'type': 'datetime'},
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
}

binary_model_quality_dict = {
    'truePositiveCount': 870,
    'falsePositiveCount': 130,
    'trueNegativeCount': 820,
    'falseNegativeCount': 180,
    **model_quality_base_dict,
}

binary_current_model_quality_dict = {
    'globalMetrics': binary_model_quality_dict,
    'groupedMetrics': {
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
    },
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
        },
        {
            'class_name': 'classB',
            'metrics': model_quality_base_dict,
        },
        {
            'class_name': 'classC',
            'metrics': model_quality_base_dict,
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

data_quality_dict = {
    'nObservations': 200,
    'classMetrics': [
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

drift_dict = {
    'featureMetrics': [
        {
            'featureName': 'gender',
            'driftCalc': {'type': 'CHI2', 'value': 0.87, 'hasDrift': True},
        },
        {
            'featureName': 'city',
            'driftCalc': {'type': 'CHI2', 'value': 0.12, 'hasDrift': False},
        },
        {
            'featureName': 'age',
            'driftCalc': {'type': 'KS', 'value': 0.92, 'hasDrift': True},
        },
    ]
}


def get_sample_reference_metrics(
    reference_uuid: uuid.UUID = REFERENCE_UUID,
    model_quality: Dict = binary_model_quality_dict,
    data_quality: Dict = data_quality_dict,
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
    data_quality: Dict = data_quality_dict,
    statistics: Dict = statistics_dict,
    drift: Dict = drift_dict,
) -> CurrentDatasetMetrics:
    return CurrentDatasetMetrics(
        current_uuid=current_uuid,
        model_quality=model_quality,
        statistics=statistics,
        data_quality=data_quality,
        drift=drift,
    )
