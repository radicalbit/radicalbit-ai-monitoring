from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from radicalbit_platform_sdk.models.job_status import JobStatus


class FileUploadResult(BaseModel):
    uuid: UUID
    path: str
    date: str
    status: JobStatus

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ReferenceFileUpload(FileUploadResult):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CurrentFileUpload(FileUploadResult):
    correlation_id_column: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class FileReference(BaseModel):
    file_url: str
    separator: str = ','
    correlation_id_column: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
