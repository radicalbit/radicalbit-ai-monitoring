from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.alias_generators import to_camel
from sqlalchemy import RowMapping

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


class TraceCount(BaseModel):
    count: int
    start_date: datetime

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class TraceTimeseriesDTO(BaseModel):
    project_uuid: UUID
    from_datetime: datetime
    to_datetime: datetime
    n: int
    traces: list[TraceCount]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )

    @staticmethod
    def from_row(
        project_uuid: UUID,
        from_datetime: datetime,
        to_datetime: datetime,
        n: int,
        interval_size_seconds: int,
        rows: list[dict],
    ) -> 'TraceTimeseriesDTO':
        start_date = from_datetime
        traces = []
        for i in range(n):
            next_date = start_date + timedelta(seconds=interval_size_seconds)
            count = [
                i['count'] for i in rows if start_date <= i['start_date'] <= next_date
            ]
            tr = TraceCount(count=count[0] if count else 0, start_date=start_date)
            traces.append(tr)
            start_date += timedelta(seconds=interval_size_seconds)
        return TraceTimeseriesDTO(
            project_uuid=project_uuid,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            n=n,
            traces=traces,
        )


class TraceCountSession(BaseModel):
    count: int
    session_uuid: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )


class SessionsTracesDTO(BaseModel):
    project_uuid: UUID
    from_datetime: datetime
    to_datetime: datetime
    traces: list[TraceCountSession]

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, from_attributes=True
    )

    @staticmethod
    def from_row(
        project_uuid: UUID,
        from_datetime: datetime,
        to_datetime: datetime,
        rows: list[RowMapping | dict],
    ) -> 'SessionsTracesDTO':
        return SessionsTracesDTO(
            project_uuid=project_uuid,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
            traces=[TraceCountSession(**i) for i in rows],
        )
