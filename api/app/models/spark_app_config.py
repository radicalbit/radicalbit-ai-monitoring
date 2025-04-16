from dataclasses import dataclass

from app.core.config.config import get_config
from app.db.tables.completion_dataset_metrics_table import CompletionDatasetMetrics
from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_embeddings_metrics_table import (
    CurrentDatasetEmbeddingsMetrics,
)
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.reference_dataset_embeddings_metrics_table import (
    ReferenceDatasetEmbeddingsMetrics,
)
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.dataset_type import DatasetType
from app.models.model_dto import ModelType


@dataclass
class SparkAppConfig:
    app_path: str
    metrics_table: str
    dataset_table: str


def get_spark_app_config(
    model_type: ModelType, dataset_type: DatasetType
) -> SparkAppConfig:
    spark_config = get_config().spark_config
    match (model_type, dataset_type):
        case (ModelType.TEXT_GENERATION, DatasetType.COMPLETION):
            return SparkAppConfig(
                app_path=spark_config.spark_completion_app_path,
                metrics_table=CompletionDatasetMetrics.__tablename__,
                dataset_table=CompletionDataset.__tablename__,
            )

        case (ModelType.EMBEDDINGS, DatasetType.REFERENCE):
            return SparkAppConfig(
                app_path=spark_config.spark_embeddings_reference_app_path,
                metrics_table=ReferenceDatasetEmbeddingsMetrics.__tablename__,
                dataset_table=ReferenceDataset.__tablename__,
            )

        case (ModelType.EMBEDDINGS, DatasetType.CURRENT):
            return SparkAppConfig(
                app_path=spark_config.spark_embeddings_current_app_path,
                metrics_table=CurrentDatasetEmbeddingsMetrics.__tablename__,
                dataset_table=CurrentDataset.__tablename__,
            )

        case (
            ModelType.BINARY
            | ModelType.MULTI_CLASS
            | ModelType.REGRESSION,
            DatasetType.REFERENCE,
        ):
            return SparkAppConfig(
                app_path=spark_config.spark_reference_app_path,
                metrics_table=ReferenceDatasetMetrics.__tablename__,
                dataset_table=ReferenceDataset.__tablename__,
            )

        case (
            ModelType.BINARY
            | ModelType.MULTI_CLASS
            | ModelType.REGRESSION,
            DatasetType.CURRENT,
        ):
            return SparkAppConfig(
                app_path=spark_config.spark_current_app_path,
                metrics_table=CurrentDatasetMetrics.__tablename__,
                dataset_table=CurrentDataset.__tablename__,
            )

        case _:
            raise ValueError(f'Unsupported combination: {model_type=} {dataset_type=}')
