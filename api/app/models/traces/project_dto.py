import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.db.tables.project_table import Project


class ProjectIn(BaseModel, validate_assignment=True):
    name: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    def to_project(self) -> Project:
        now = datetime.datetime.now(tz=datetime.UTC)
        return Project(
            name=self.name,
            created_at=now,
            updated_at=now,
        )


class ProjectOut(BaseModel):
    uuid: UUID
    name: str
    created_at: str
    updated_at: str
    traces: Optional[int]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_project(project: Project, traces: Optional[int] = None):
        return ProjectOut(
            uuid=project.uuid,
            name=project.name,
            created_at=str(project.created_at),
            updated_at=str(project.updated_at),
            traces=traces,
        )
