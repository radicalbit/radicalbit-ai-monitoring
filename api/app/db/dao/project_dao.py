from db.tables.project_table import Project

from app.db.database import Database


class ProjectDAO:
    def __init__(self, database: Database):
        self.db = database

    def insert(self, project: Project) -> Project:
        with self.db.begin_session() as session:
            session.add(project)
            session.flush()
            return project
