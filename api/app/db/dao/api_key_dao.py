from typing import Optional
from uuid import UUID

from app.db.database import Database
from app.db.tables.api_key_table import ApiKey


class ApiKeyDAO:
    def __init__(self, database: Database):
        self.db = database

    def insert(self, api_key: ApiKey) -> ApiKey:
        with self.db.begin_session() as session:
            session.add(api_key)
            session.flush()
            return api_key

    def get_by_uuid(self, project_uuid: UUID, key: str) -> Optional[ApiKey]:
        pass
