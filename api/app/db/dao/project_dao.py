from typing import Optional
from uuid import UUID

from app.db.database import Database
from app.db.tables.project_table import Project


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
