from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.reference_dataset_table import ReferenceDataset


class ReferenceDatasetDTO(BaseModel):
    uuid: UUID
    model_uuid: UUID
    path: str
    date: str
    status: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_reference_dataset(rd: ReferenceDataset) -> 'ReferenceDatasetDTO':
        return ReferenceDatasetDTO(
            uuid=rd.uuid,
            model_uuid=rd.model_uuid,
            path=rd.path,
            date=rd.date.isoformat(),
            status=rd.status,
        )


class CurrentDatasetDTO(BaseModel):
    uuid: UUID
    model_uuid: UUID
    path: str
    date: str
    correlation_id_column: Optional[str]
    status: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_current_dataset(cd: CurrentDataset) -> 'CurrentDatasetDTO':
        return CurrentDatasetDTO(
            uuid=cd.uuid,
            model_uuid=cd.model_uuid,
            path=cd.path,
            date=cd.date.isoformat(),
            correlation_id_column=cd.correlation_id_column,
            status=cd.status,
        )


class CompletionDatasetDTO(BaseModel):
    uuid: UUID
    model_uuid: UUID
    path: str
    date: str
    status: str

    model_config = ConfigDict(
        populate_by_name=True, alias_generator=to_camel, protected_namespaces=()
    )

    @staticmethod
    def from_completion_dataset(cd: CompletionDataset) -> 'CompletionDatasetDTO':
        return CompletionDatasetDTO(
            uuid=cd.uuid,
            model_uuid=cd.model_uuid,
            path=cd.path,
            date=cd.date.isoformat(),
            status=cd.status,
        )


class FileReference(BaseModel):
    file_url: str
    separator: str = ','
    correlation_id_column: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class OrderType(str, Enum):
    ASC = 'asc'
    DESC = 'desc'
