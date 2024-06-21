from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.models import (
    ModelType,
    CurrentFileUpload,
    JobStatus,
    DatasetStats,
)
from radicalbit_platform_sdk.errors import ClientError
from pydantic import ValidationError
from typing import Optional
import requests
from uuid import UUID


class ModelCurrentDataset:
    def __init__(
        self,
        base_url: str,
        model_uuid: UUID,
        model_type: ModelType,
        upload: CurrentFileUpload,
    ) -> None:
        self.__base_url = base_url
        self.__model_uuid = model_uuid
        self.__model_type = model_type
        self.__uuid = upload.uuid
        self.__path = upload.path
        self.__correlation_id_column = upload.correlation_id_column
        self.__date = upload.date
        self.__status = upload.status
        self.__statistics = None
        self.__model_metrics = None
        self.__data_metrics = None
        self.__drift = None

    def uuid(self) -> UUID:
        return self.__uuid

    def path(self) -> str:
        return self.__path

    def correlation_id_column(self) -> str:
        return self.__correlation_id_column

    def date(self) -> str:
        return self.__date

    def status(self) -> str:
        return self.__status

    def statistics(self) -> Optional[DatasetStats]:
        """
        Get statistics about the current dataset

        :return: The `DatasetStats` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[DatasetStats]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "statistics" in response_json:
                    return job_status, DatasetStats.model_validate(
                        response_json["statistics"]
                    )
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        match self.__status:
            case JobStatus.ERROR:
                self.__statistics = None
            case JobStatus.SUCCEEDED:
                if self.__statistics is None:
                    _, stats = invoke(
                        method="GET",
                        url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/statistics",
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__statistics = stats
            case JobStatus.IMPORTING:
                status, stats = invoke(
                    method="GET",
                    url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/statistics",
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__statistics = stats

        return self.__statistics

    def drift(self):
        # TODO: implement get drift
        pass

    def data_quality(self):
        # TODO: implement get data quality
        pass

    def model_quality(self):
        # TODO: implement get model quality
        pass
