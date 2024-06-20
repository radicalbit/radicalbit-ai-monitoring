from typing import Optional
from uuid import UUID

from app.db.database import Database
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset


class CurrentDatasetMetricsDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_current_dataset_metrics(
        self, current_dataset_metrics: CurrentDatasetMetrics
    ) -> CurrentDatasetMetrics:
        with self.db.begin_session() as session:
            session.add(current_dataset_metrics)
            session.flush()
            return current_dataset_metrics

    def get_current_metrics_by_model_uuid(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> Optional[CurrentDatasetMetrics]:
        with self.db.begin_session() as session:
            return (
                session.query(CurrentDatasetMetrics)
                .join(
                    CurrentDataset,
                    CurrentDatasetMetrics.current_uuid == CurrentDataset.uuid,
                )
                .where(
                    CurrentDataset.model_uuid == model_uuid,
                    CurrentDataset.uuid == current_uuid,
                )
                .one_or_none()
            )
