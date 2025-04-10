import re
from typing import Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select, Sequence, asc, desc, select

from app.db.database import Database
from app.db.tables.api_key_table import ApiKey
from app.models.commons.order_type import OrderType


class ApiKeyDAO:
    def __init__(self, database: Database):
        self.db = database

    @staticmethod
    def _get_all_stmt(project_uuid: UUID) -> Select:
        return select(ApiKey).where(
            ApiKey.project_uuid == project_uuid, ApiKey.deleted.is_(False)
        )

    def insert(self, api_key: ApiKey) -> ApiKey:
        with self.db.begin_session() as session:
            session.add(api_key)
            session.flush()
            return api_key

    def get_all(self, project_uuid: UUID) -> Sequence[ApiKey]:
        with self.db.begin_session() as session:
            stmt = self._get_all_stmt(project_uuid=project_uuid)
            return session.scalars(stmt).all()

    def get_all_paginated(
        self,
        project_uuid: UUID,
        params: Optional[Params] = None,
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ApiKey]:
        def order_by_column_name(column_name: str):
            snake_case_column = re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower()
            return getattr(ApiKey, snake_case_column)

        if params is None:
            params = Params()

        with self.db.begin_session() as session:
            stmt = self._get_all_stmt(project_uuid=project_uuid)
            if sort:
                stmt = (
                    stmt.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else stmt.order_by(desc(order_by_column_name(sort)))
                )
            return paginate(session, stmt, params)

    def get_api_key(self, project_uuid: UUID, name: str) -> ApiKey:
        with self.db.begin_session() as session:
            return session.scalar(
                select(ApiKey).where(
                    ApiKey.name == name,
                    ApiKey.project_uuid == project_uuid,
                    ApiKey.deleted.is_(False),
                )
            )

    def get_by_hashed_key(self, hashed_key: str) -> Optional[ApiKey]:
        with self.db.begin_session() as session:
            stmt = select(ApiKey).where(ApiKey.hashed_key == hashed_key)
            return session.scalar(stmt)
