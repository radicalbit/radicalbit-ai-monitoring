import uuid as uuid_lib

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseProjectDefinition(BaseModel):
    """A base class for project definition.

    Attributes:
        name: The name of the project.

    """

    name: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class CreateProject(BaseProjectDefinition):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ProjectDefinition(BaseProjectDefinition):
    uuid: uuid_lib.UUID = Field(default_factory=lambda: uuid_lib.uuid4())
    created_at: str = Field(alias='createdAt')
    updated_at: str = Field(alias='updatedAt')

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
