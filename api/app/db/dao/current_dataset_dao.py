import re
from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc
from sqlalchemy.future import select as future_select

from app.db.database import Database
from app.db.tables.current_dataset_table import CurrentDataset
from app.models.dataset_dto import OrderType


class CurrentDatasetDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_current_dataset(self, current_dataset: CurrentDataset) -> CurrentDataset:
        with self.db.begin_session() as session:
            session.add(current_dataset)
            session.flush()
            return current_dataset

    def get_current_dataset_by_model_uuid(
        self, model_uuid: UUID, current_uuid: UUID
    ) -> Optional[CurrentDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(CurrentDataset)
                .where(
                    CurrentDataset.model_uuid == model_uuid,
                    CurrentDataset.uuid == current_uuid,
                )
                .one_or_none()
            )

    def get_latest_current_dataset_by_model_uuid(
        self, model_uuid: UUID
    ) -> Optional[CurrentDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(CurrentDataset)
                .order_by(desc(CurrentDataset.date))
                .where(CurrentDataset.model_uuid == model_uuid)
                .limit(1)
                .one_or_none()
            )

    def get_all_current_datasets_by_model_uuid(
        self,
        model_uuid: UUID,
    ) -> List[CurrentDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(CurrentDataset)
                .order_by(desc(CurrentDataset.date))
                .where(CurrentDataset.model_uuid == model_uuid)
            )

    def get_all_current_datasets_by_model_uuid_paginated(
        self,
        model_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[CurrentDataset]:
        def order_by_column_name(column_name):
            return CurrentDataset.__getattribute__(
                CurrentDataset, re.sub('(?=[A-Z])', '_', column_name).lower()
            )

        with self.db.begin_session() as session:
            stmt = future_select(CurrentDataset).where(
                CurrentDataset.model_uuid == model_uuid
            )

            if sort:
                stmt = (
                    stmt.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else stmt.order_by(desc(order_by_column_name(sort)))
                )

            return paginate(session, stmt, params)
