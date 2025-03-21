from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel

from app.models.utils import nano_to_millis


class LatenciesWidgetDTO(BaseModel):
    project_uuid: UUID
    session_uuid: Optional[UUID] = None
    span_name: Optional[str] = None
    p50: float = Field(exclude=True)
    p90: float = Field(exclude=True)
    p95: float = Field(exclude=True)
    p99: float = Field(exclude=True)

    @computed_field
    def p50_ms(self) -> float:
        return nano_to_millis(self.p50)

    @computed_field
    def p90_ms(self) -> float:
        return nano_to_millis(self.p90)

    @computed_field
    def p95_ms(self) -> float:
        return nano_to_millis(self.p95)

    @computed_field
    def p99_ms(self) -> float:
        return nano_to_millis(self.p99)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
