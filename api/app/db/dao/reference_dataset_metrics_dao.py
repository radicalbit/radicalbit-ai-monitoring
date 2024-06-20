from typing import Dict, Optional
from uuid import UUID

import sqlalchemy

from app.db.database import Database
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset


class ReferenceDatasetMetricsDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_reference_metrics(
        self, reference_metrics: ReferenceDatasetMetrics
    ) -> ReferenceDatasetMetrics:
        with self.db.begin_session() as session:
            session.add(reference_metrics)
            session.flush()
            return reference_metrics

    def get_reference_metrics_by_model_uuid(
        self, model_uuid: UUID
    ) -> Optional[ReferenceDatasetMetrics]:
        with self.db.begin_session() as session:
            return (
                session.query(ReferenceDatasetMetrics)
                .join(
                    ReferenceDataset,
                    ReferenceDatasetMetrics.reference_uuid == ReferenceDataset.uuid,
                )
                .where(ReferenceDataset.model_uuid == model_uuid)
                .one_or_none()
            )

    def get_reference_metrics_by_reference_uuid(
        self, reference_uuid: UUID
    ) -> Optional[ReferenceDatasetMetrics]:
        with self.db.begin_session() as session:
            return (
                session.query(ReferenceDatasetMetrics)
                .where(ReferenceDatasetMetrics.reference_uuid == reference_uuid)
                .one_or_none()
            )

    def update_reference_model_quality(
        self, reference_uuid: UUID, model_quality: Dict
    ) -> int:
        with self.db.begin_session() as session:
            query = (
                sqlalchemy.update(ReferenceDatasetMetrics)
                .where(ReferenceDatasetMetrics.reference_uuid == reference_uuid)
                .values(model_quality=model_quality)
            )
            return session.execute(query).rowcount

    def update_reference_data_quality(
        self, reference_uuid: UUID, data_quality: Dict
    ) -> int:
        with self.db.begin_session() as session:
            query = (
                sqlalchemy.update(ReferenceDatasetMetrics)
                .where(ReferenceDatasetMetrics.reference_uuid == reference_uuid)
                .values(data_quality=data_quality)
            )
            return session.execute(query).rowcount

    def update_reference_statistics(
        self, reference_uuid: UUID, statistics: Dict
    ) -> int:
        with self.db.begin_session() as session:
            query = (
                sqlalchemy.update(ReferenceDatasetMetrics)
                .where(ReferenceDatasetMetrics.reference_uuid == reference_uuid)
                .values(statistics=statistics)
            )
            return session.execute(query).rowcount
