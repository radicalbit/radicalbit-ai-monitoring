import datetime
import re
from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
import sqlalchemy
from sqlalchemy import asc, delete, desc
from sqlalchemy.future import select as future_select

from app.db.database import Database
from app.db.tables.api_key_table import ApiKey
from app.db.tables.project_table import Project
from app.models.commons.order_type import OrderType


class ProjectDAO:
    def __init__(self, database: Database):
        self.db = database

    def insert(self, project: Project) -> Project:
        with self.db.begin_session() as session:
            session.add(project)
            session.flush()
            return project

    def get_by_uuid(self, uuid: UUID) -> Optional[Project]:
        with self.db.begin_session() as session:
            return (
                session.query(Project)
                .where(Project.uuid == uuid, Project.deleted.is_(False))
                .one_or_none()
            )

    def get_all(self) -> List[Project]:
        with self.db.begin_session() as session:
            return session.query(Project).where(Project.deleted.is_(False))

    def get_all_paginated(
        self,
        params: Optional[Params] = None,
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[Project]:
        def order_by_column_name(column_name: str):
            snake_case_column = re.sub(r'(?<!^)(?=[A-Z])', '_', column_name).lower()
            return getattr(Project, snake_case_column)

        if params is None:
            params = Params()

        with self.db.begin_session() as session:
            stmt = future_select(Project).filter(Project.deleted.is_(False))

            if sort:
                stmt = (
                    stmt.order_by(asc(order_by_column_name(sort)))
                    if order == OrderType.ASC
                    else stmt.order_by(desc(order_by_column_name(sort)))
                )

            return paginate(session, stmt, params)

    def update(self, project: Project) -> int:
        with self.db.begin_session() as session:
            project.updated_at = datetime.datetime.now(tz=datetime.UTC)
            query = (
                sqlalchemy.update(Project)
                .where(Project.uuid == project.uuid, Project.deleted.is_(False))
                .values(**project.attributes())
            )
            return session.execute(query).rowcount

    def delete(self, uuid: UUID) -> int:
        with self.db.begin_session() as session:
            deleted_at = datetime.datetime.now(tz=datetime.UTC)
            query = (
                sqlalchemy.update(Project)
                .where(Project.uuid == uuid, Project.deleted.is_(False))
                .values(deleted=True, updated_at=deleted_at)
            )
            delete_api_key = delete(ApiKey).where(
                ApiKey.project_uuid == uuid,
            )
            session.execute(delete_api_key)
            return session.execute(query).rowcount
