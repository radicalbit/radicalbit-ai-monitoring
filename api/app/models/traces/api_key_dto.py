from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, computed_field
from pydantic.alias_generators import to_camel

from app.db.tables.api_key_table import ApiKey


class ApiKeySec(BaseModel):
    plain_key: str
    hashed_key: str

    @computed_field(return_type=str)
    def obscured_key(self) -> str:
        return self.plain_key[:8] + '*' * 43 + self.plain_key[-3:]


class ApiKeyIn(BaseModel):
    name: str = 'default'

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    def to_api_key(self, hashed_key: str, obscured_key: str) -> ApiKey:
        now = datetime.now(tz=timezone.utc)
        return ApiKey(
            name=self.name,
            hashed_key=hashed_key,
            obscured_key=obscured_key,
            created_at=now,
            updated_at=now,
        )


class ApiKeyOut(BaseModel):
    name: str
    api_key: str
    created_at: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_api_key(api_key: ApiKey, plain_api_key: str) -> 'ApiKeyOut':
        return ApiKeyOut(
            name=api_key.name,
            api_key=plain_api_key,
            created_at=str(api_key.created_at),
        )
