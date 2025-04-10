from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseApiKeyDefinition(BaseModel):
    """A base class for api_key definition.

    Attributes:
        name: The name of the api_key.

    """

    name: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )


class CreateApiKey(BaseApiKeyDefinition):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ApiKeyDefinition(BaseApiKeyDefinition):
    api_key: str
    project_uuid: UUID
    created_at: str
    updated_at: str

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)
