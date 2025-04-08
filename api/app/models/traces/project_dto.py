import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.db.tables.api_key_table import ApiKey
from app.db.tables.project_table import Project
from app.models.traces.api_key_dto import ApiKeyOut


class ProjectIn(BaseModel, validate_assignment=True):
    name: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    def to_project(self, hashed_key: str, obscured_key: str) -> Project:
        now = datetime.datetime.now(tz=datetime.UTC)
        api_key = ApiKey(
            name='default',
            hashed_key=hashed_key,
            obscured_key=obscured_key,
            created_at=now,
            updated_at=now,
        )
        return Project(
            name=self.name, created_at=now, updated_at=now, api_keys=[api_key]
        )


class ProjectOut(BaseModel):
    uuid: UUID
    name: str
    created_at: str
    updated_at: str
    traces: Optional[int]
    api_key: Optional[ApiKeyOut]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_project(
        project: Project,
        plain_api_key: Optional[str] = None,
        traces: Optional[int] = None,
    ) -> 'ProjectOut':
        api_key_out = None
        if plain_api_key:
            api_key_out = ApiKeyOut.from_api_key(
                api_key=project.api_keys[0],
                plain_api_key=plain_api_key,
                project_uuid=project.uuid,
            )
        return ProjectOut(
            uuid=project.uuid,
            name=project.name,
            created_at=str(project.created_at),
            updated_at=str(project.updated_at),
            traces=traces,
            api_key=api_key_out,
        )
