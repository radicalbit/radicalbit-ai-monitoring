from typing import Optional
from uuid import UUID

from app.db.database import Database
from app.db.tables.reference_dataset_embeddings_metrics_table import (
    ReferenceDatasetEmbeddingsMetrics,
)
from app.db.tables.reference_dataset_table import ReferenceDataset


class ReferenceDatasetEmbeddingsMetricsDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_reference_embeddings_metrics(
        self, reference_embeddings_metrics: ReferenceDatasetEmbeddingsMetrics
    ) -> ReferenceDatasetEmbeddingsMetrics:
        with self.db.begin_session() as session:
            session.add(reference_embeddings_metrics)
            session.flush()
            return reference_embeddings_metrics

    def get_reference_embeddings_metrics_by_model_uuid(
        self, model_uuid: UUID
    ) -> Optional[ReferenceDatasetEmbeddingsMetrics]:
        with self.db.begin_session() as session:
            return (
                session.query(ReferenceDatasetEmbeddingsMetrics)
                .join(
                    ReferenceDataset,
                    ReferenceDatasetEmbeddingsMetrics.reference_uuid
                    == ReferenceDataset.uuid,
                )
                .where(ReferenceDataset.model_uuid == model_uuid)
                .one_or_none()
            )
