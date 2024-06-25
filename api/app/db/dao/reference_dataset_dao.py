import re
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc
from sqlalchemy.future import select as future_select

from app.db.database import Database
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.dataset_dto import OrderType


class ReferenceDatasetDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_reference_dataset(
        self, reference_dataset: ReferenceDataset
    ) -> ReferenceDataset:
        with self.db.begin_session() as session:
            session.add(reference_dataset)
            session.flush()
            return reference_dataset

    def get_reference_dataset_by_model_uuid(
        self, model_uuid: UUID
    ) -> Optional[ReferenceDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(ReferenceDataset)
                .where(ReferenceDataset.model_uuid == model_uuid)
                .one_or_none()
            )

    def get_latest_reference_dataset_by_model_uuid(
        self, model_uuid: UUID
    ) -> Optional[ReferenceDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(ReferenceDataset)
                .order_by(desc(ReferenceDataset.date))
                .where(ReferenceDataset.model_uuid == model_uuid)
                .limit(1)
                .one_or_none()
            )

    def get_all_reference_datasets_by_model_uuid(
        self,
        model_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ReferenceDataset]:
        def order_by_column_name(column_name):
            return ReferenceDataset.__getattribute__(
                ReferenceDataset, re.sub('(?=[A-Z])', '_', column_name).lower()
            )

        with self.db.begin_session() as session:
            stmt = future_select(ReferenceDataset).where(
                ReferenceDataset.model_uuid == model_uuid
            )

            if sort:
                stmt = (
                    stmt.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else stmt.order_by(desc(order_by_column_name(sort)))
                )

            return paginate(session, stmt, params)
