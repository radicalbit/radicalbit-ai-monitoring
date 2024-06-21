from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.models import (
    JobStatus,
    ReferenceFileUpload,
    DatasetStats,
    ModelQuality,
    DataQuality,
    ModelType,
    BinaryClassificationModelQuality,
    BinaryClassificationDataQuality,
)
from radicalbit_platform_sdk.errors import ClientError
from pydantic import ValidationError
from typing import Optional
import requests
from uuid import UUID


class ModelReferenceDataset:
    def __init__(
        self,
        base_url: str,
        model_uuid: UUID,
        model_type: ModelType,
        upload: ReferenceFileUpload,
    ) -> None:
        self.__base_url = base_url
        self.__model_uuid = model_uuid
        self.__model_type = model_type
        self.__uuid = upload.uuid
        self.__path = upload.path
        self.__date = upload.date
        self.__status = upload.status
        self.__statistics = None
        self.__model_metrics = None
        self.__data_metrics = None

    def uuid(self) -> UUID:
        return self.__uuid

    def path(self) -> str:
        return self.__path

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
                        url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/statistics",
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__statistics = stats
            case JobStatus.IMPORTING:
                status, stats = invoke(
                    method="GET",
                    url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/statistics",
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__statistics = stats

        return self.__statistics

    def data_quality(self) -> Optional[DataQuality]:
        """
        Get data quality metrics about the current dataset

        :return: The `DataQuality` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[DataQuality]]:
            try:
                print(response.text)
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "dataQuality" in response_json:
                    if self.__model_type is ModelType.BINARY:
                        return (
                            job_status,
                            BinaryClassificationDataQuality.model_validate(
                                response_json["dataQuality"]
                            ),
                        )
                    else:
                        raise ClientError(
                            "Unable to parse get metrics for not binary models"
                        )
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        match self.__status:
            case JobStatus.ERROR:
                self.__data_metrics = None
            case JobStatus.SUCCEEDED:
                if self.__data_metrics is None:
                    _, metrics = invoke(
                        method="GET",
                        url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/data-quality",
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__data_metrics = metrics
            case JobStatus.IMPORTING:
                status, metrics = invoke(
                    method="GET",
                    url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/data-quality",
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__data_metrics = metrics

        return self.__data_metrics

    def model_quality(self) -> Optional[ModelQuality]:
        """
        Get model quality metrics about the current dataset

        :return: The `ModelQuality` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[ModelQuality]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json["jobStatus"])
                if "modelQuality" in response_json:
                    if self.__model_type is ModelType.BINARY:
                        return (
                            job_status,
                            BinaryClassificationModelQuality.model_validate(
                                response_json["modelQuality"]
                            ),
                        )
                    else:
                        raise ClientError(
                            "Unable to parse get metrics for not binary models"
                        )
                else:
                    return job_status, None
            except KeyError as _:
                raise ClientError(f"Unable to parse response: {response.text}")
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        match self.__status:
            case JobStatus.ERROR:
                self.__model_metrics = None
            case JobStatus.SUCCEEDED:
                if self.__model_metrics is None:
                    _, metrics = invoke(
                        method="GET",
                        url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/model-quality",
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__model_metrics = metrics
            case JobStatus.IMPORTING:
                status, metrics = invoke(
                    method="GET",
                    url=f"{self.__base_url}/api/models/{str(self.__model_uuid)}/reference/model-quality",
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__model_metrics = metrics

        return self.__model_metrics
