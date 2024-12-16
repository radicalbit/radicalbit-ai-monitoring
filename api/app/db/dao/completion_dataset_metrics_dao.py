from typing import Optional
from uuid import UUID

from app.db.database import Database
from app.db.tables.completion_dataset_metrics_table import CompletionDatasetMetrics
from app.db.tables.completion_dataset_table import CompletionDataset


class CompletionDatasetMetricsDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_completion_metrics(
        self, completion_metrics: CompletionDatasetMetrics
    ) -> CompletionDatasetMetrics:
        with self.db.begin_session() as session:
            session.add(completion_metrics)
            session.flush()
            return completion_metrics

    def get_completion_metrics_by_model_uuid(
        self, model_uuid: UUID, completion_uuid: UUID
    ) -> Optional[CompletionDatasetMetrics]:
        with self.db.begin_session() as session:
            return (
                session.query(CompletionDatasetMetrics)
                .join(
                    CompletionDataset,
                    CompletionDatasetMetrics.completion_uuid == CompletionDataset.uuid,
                )
                .where(
                    CompletionDataset.model_uuid == model_uuid,
                    CompletionDataset.uuid == completion_uuid,
                )
                .one_or_none()
            )
