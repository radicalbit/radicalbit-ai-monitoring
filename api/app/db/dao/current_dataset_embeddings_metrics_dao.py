from typing import Optional
from uuid import UUID

from app.db.database import Database
from app.db.tables.current_dataset_embeddings_metrics_table import (
    CurrentDatasetEmbeddingsMetrics,
)
from app.db.tables.current_dataset_table import CurrentDataset


class CurrentDatasetEmbeddingsMetricsDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_current_dataset_embeddings_metrics(
        self, current_dataset_embeddings_metrics: CurrentDatasetEmbeddingsMetrics
    ) -> CurrentDatasetEmbeddingsMetrics:
        with self.db.begin_session() as session:
            session.add(current_dataset_embeddings_metrics)
            session.flush()
            return current_dataset_embeddings_metrics

    def get_current_embeddings_metrics_by_model_uuid(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> Optional[CurrentDatasetEmbeddingsMetrics]:
        with self.db.begin_session() as session:
            return (
                session.query(CurrentDatasetEmbeddingsMetrics)
                .join(
                    CurrentDataset,
                    CurrentDatasetEmbeddingsMetrics.current_uuid == CurrentDataset.uuid,
                )
                .where(
                    CurrentDataset.model_uuid == model_uuid,
                    CurrentDataset.uuid == current_uuid,
                )
                .one_or_none()
            )
