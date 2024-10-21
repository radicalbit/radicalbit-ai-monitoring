import datetime
import re
from typing import Dict, List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
import sqlalchemy
from sqlalchemy import asc, desc, func
from sqlalchemy.future import select as future_select

from app.db.database import Database
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.model_table import Model
from app.models.model_order import OrderType


class ModelDAO:
    def __init__(self, database: Database):
        self.db = database

    def insert(self, model: Model) -> Model:
        with self.db.begin_session() as session:
            session.add(model)
            session.flush()
            return model

    def get_by_uuid(self, uuid: UUID) -> Optional[Model]:
        with self.db.begin_session() as session:
            return (
                session.query(Model)
                .where(Model.uuid == uuid, Model.deleted.is_(False))
                .one_or_none()
            )

    def update_features(self, uuid: UUID, model_features: List[Dict]):
        with self.db.begin_session() as session:
            query = (
                sqlalchemy.update(Model)
                .where(Model.uuid == uuid)
                .values(features=model_features)
            )
            return session.execute(query).rowcount

    def delete(self, uuid: UUID) -> int:
        with self.db.begin_session() as session:
            deleted_at = datetime.datetime.now(tz=datetime.UTC)
            query = (
                sqlalchemy.update(Model)
                .where(Model.uuid == uuid, Model.deleted.is_(False))
                .values(deleted=True, updated_at=deleted_at)
            )
            return session.execute(query).rowcount

    def get_all(
        self,
    ) -> List[Model]:
        with self.db.begin_session() as session:
            return session.query(Model).where(Model.deleted.is_(False))

    def get_last_n_percentages(self, n_models=None):
        with self.db.begin_session() as session:
            subq = (
                session.query(
                    CurrentDataset.model_uuid,
                    func.max(CurrentDataset.date).label('maxdate'),
                )
                .group_by(CurrentDataset.model_uuid)
                .subquery()
            )
            stmt = (
                session.query(Model, CurrentDatasetMetrics)
                .join(
                    CurrentDataset,
                    CurrentDataset.model_uuid == Model.uuid,
                )
                .join(
                    subq,
                    (CurrentDataset.model_uuid == subq.c.model_uuid)
                    & (CurrentDataset.date == subq.c.maxdate),
                )
                .join(
                    CurrentDatasetMetrics,
                    CurrentDatasetMetrics.current_uuid == CurrentDataset.uuid,
                )
                .order_by(Model.updated_at.desc())
            )
            if n_models:
                stmt = stmt.limit(n_models)
            return stmt.all()

    def get_all_paginated(
        self,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[Model]:
        def order_by_column_name(column_name):
            return Model.__getattribute__(
                Model, re.sub('(?=[A-Z])', '_', column_name).lower()
            )

        with self.db.begin_session() as session:
            subq = (
                session.query(
                    CurrentDataset.model_uuid,
                    func.max(CurrentDataset.date).label('maxdate'),
                )
                .group_by(CurrentDataset.model_uuid)
                .subquery()
            )
            subq2 = (
                session.query(CurrentDataset.uuid, CurrentDataset.model_uuid)
                .join(
                    subq,
                    (CurrentDataset.model_uuid == subq.c.model_uuid)
                    & (CurrentDataset.date == subq.c.maxdate),
                )
                .subquery()
            )
            stmt = (
                future_select(Model, CurrentDatasetMetrics)
                .outerjoin(
                    subq2,
                    subq2.c.model_uuid == Model.uuid,
                )
                .outerjoin(
                    CurrentDatasetMetrics,
                    CurrentDatasetMetrics.current_uuid == subq2.c.uuid,
                )
                .filter(Model.deleted.is_(False))
            )

            if sort:
                stmt = (
                    stmt.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else stmt.order_by(desc(order_by_column_name(sort)))
                )

            return paginate(session, stmt, params)
