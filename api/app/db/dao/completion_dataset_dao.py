import re
from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc
from sqlalchemy.future import select as future_select

from app.db.database import Database
from app.db.tables.completion_dataset_table import CompletionDataset
from app.models.commons.order_type import OrderType


class CompletionDatasetDAO:
    def __init__(self, database: Database) -> None:
        self.db = database

    def insert_completion_dataset(
        self, completion_dataset: CompletionDataset
    ) -> CompletionDataset:
        with self.db.begin_session() as session:
            session.add(completion_dataset)
            session.flush()
            return completion_dataset

    def get_completion_dataset_by_model_uuid(
        self, model_uuid: UUID, completion_uuid: UUID
    ) -> Optional[CompletionDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(CompletionDataset)
                .where(
                    CompletionDataset.model_uuid == model_uuid,
                    CompletionDataset.uuid == completion_uuid,
                )
                .one_or_none()
            )

    def get_latest_completion_dataset_by_model_uuid(
        self, model_uuid: UUID
    ) -> Optional[CompletionDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(CompletionDataset)
                .order_by(desc(CompletionDataset.date))
                .where(CompletionDataset.model_uuid == model_uuid)
                .limit(1)
                .one_or_none()
            )

    def get_all_completion_datasets_by_model_uuid(
        self,
        model_uuid: UUID,
    ) -> List[CompletionDataset]:
        with self.db.begin_session() as session:
            return (
                session.query(CompletionDataset)
                .order_by(desc(CompletionDataset.date))
                .where(CompletionDataset.model_uuid == model_uuid)
            )

    def get_all_completion_datasets_by_model_uuid_paginated(
        self,
        model_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[CompletionDataset]:
        def order_by_column_name(column_name):
            return CompletionDataset.__getattribute__(
                CompletionDataset, re.sub('(?=[A-Z])', '_', column_name).lower()
            )

        with self.db.begin_session() as session:
            stmt = future_select(CompletionDataset).where(
                CompletionDataset.model_uuid == model_uuid
            )

            if sort:
                stmt = (
                    stmt.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else stmt.order_by(desc(order_by_column_name(sort)))
                )

            return paginate(session, stmt, params)
