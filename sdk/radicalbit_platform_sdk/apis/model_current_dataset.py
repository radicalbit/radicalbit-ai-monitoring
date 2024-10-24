from typing import Optional
from uuid import UUID

from pydantic import ValidationError
import requests

from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    ClassificationDataQuality,
    CurrentBinaryClassificationModelQuality,
    CurrentFileUpload,
    CurrentMultiClassificationModelQuality,
    CurrentRegressionModelQuality,
    DataQuality,
    DatasetStats,
    Drift,
    JobStatus,
    ModelQuality,
    ModelType,
    RegressionDataQuality,
)
from radicalbit_platform_sdk.models.dataset_percentages import Percentages


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
        self.__percentages = None

    def uuid(self) -> UUID:
        return self.__uuid

    def path(self) -> str:
        return self.__path

    def correlation_id_column(self) -> Optional[str]:
        return self.__correlation_id_column

    def date(self) -> str:
        return self.__date

    def status(self) -> str:
        return self.__status

    def statistics(self) -> Optional[DatasetStats]:
        """Get statistics about the actual dataset

        :return: The `DatasetStats` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[DatasetStats]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json['jobStatus'])
                if 'statistics' in response_json:
                    return job_status, DatasetStats.model_validate(
                        response_json['statistics']
                    )

            except KeyError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            else:
                return job_status, None

        match self.__status:
            case JobStatus.ERROR:
                self.__statistics = None
            case JobStatus.MISSING_CURRENT:
                self.__statistics = None
            case JobStatus.SUCCEEDED:
                if self.__statistics is None:
                    _, stats = invoke(
                        method='GET',
                        url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/statistics',
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__statistics = stats
            case JobStatus.IMPORTING:
                status, stats = invoke(
                    method='GET',
                    url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/statistics',
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__statistics = stats

        return self.__statistics

    def percentages(self) -> Optional[Percentages]:
        """Get percentages about the actual dataset

        :return: The `Percentages` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[Percentages]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json['jobStatus'])
                if 'percentages' in response_json:
                    return (
                        job_status,
                        Percentages.model_validate(response_json['percentages']),
                    )
            except KeyError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            else:
                return job_status, None

        match self.__status:
            case JobStatus.ERROR:
                self.__percentages = None
            case JobStatus.MISSING_CURRENT:
                self.__percentages = None
            case JobStatus.SUCCEEDED:
                if self.__percentages is None:
                    _, percentages = invoke(
                        method='GET',
                        url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/percentages',
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__percentages = percentages
            case JobStatus.IMPORTING:
                status, percentages = invoke(
                    method='GET',
                    url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/percentages',
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__percentages = percentages

        return self.__percentages

    def drift(self) -> Optional[Drift]:
        """Get drift about the actual dataset

        :return: The `Drift` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[Drift]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json['jobStatus'])
                if 'drift' in response_json:
                    return (
                        job_status,
                        Drift.model_validate(response_json['drift']),
                    )
            except KeyError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            else:
                return job_status, None

        match self.__status:
            case JobStatus.ERROR:
                self.__drift = None
            case JobStatus.MISSING_CURRENT:
                self.__drift = None
            case JobStatus.SUCCEEDED:
                if self.__drift is None:
                    _, drift = invoke(
                        method='GET',
                        url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/drift',
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__drift = drift
            case JobStatus.IMPORTING:
                status, drift = invoke(
                    method='GET',
                    url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/drift',
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__drift = drift

        return self.__drift

    def data_quality(self) -> Optional[DataQuality]:
        """Get data quality metrics about the actual dataset

        :return: The `DataQuality` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[DataQuality]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json['jobStatus'])
                if 'dataQuality' in response_json:
                    match self.__model_type:
                        case ModelType.BINARY | ModelType.MULTI_CLASS:
                            return (
                                job_status,
                                ClassificationDataQuality.model_validate(
                                    response_json['dataQuality']
                                ),
                            )
                        case ModelType.REGRESSION:
                            return (
                                job_status,
                                RegressionDataQuality.model_validate(
                                    response_json['dataQuality']
                                ),
                            )
                        case _:
                            raise ClientError(
                                'Unable to parse metrics because of not managed model type'
                            ) from None
            except KeyError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            else:
                return job_status, None

        match self.__status:
            case JobStatus.ERROR:
                self.__data_metrics = None
            case JobStatus.MISSING_CURRENT:
                self.__data_metrics = None
            case JobStatus.SUCCEEDED:
                if self.__data_metrics is None:
                    _, metrics = invoke(
                        method='GET',
                        url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/data-quality',
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__data_metrics = metrics
            case JobStatus.IMPORTING:
                status, metrics = invoke(
                    method='GET',
                    url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/data-quality',
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__data_metrics = metrics

        return self.__data_metrics

    def model_quality(self) -> Optional[ModelQuality]:
        """Get model quality metrics about the actual dataset

        :return: The `ModelQuality` if exists
        """

        def __callback(
            response: requests.Response,
        ) -> tuple[JobStatus, Optional[ModelQuality]]:
            try:
                response_json = response.json()
                job_status = JobStatus(response_json['jobStatus'])
                if 'modelQuality' in response_json:
                    match self.__model_type:
                        case ModelType.BINARY:
                            return (
                                job_status,
                                CurrentBinaryClassificationModelQuality.model_validate(
                                    response_json['modelQuality']
                                ),
                            )
                        case ModelType.MULTI_CLASS:
                            return (
                                job_status,
                                CurrentMultiClassificationModelQuality.model_validate(
                                    response_json['modelQuality']
                                ),
                            )
                        case ModelType.REGRESSION:
                            return (
                                job_status,
                                CurrentRegressionModelQuality.model_validate(
                                    response_json['modelQuality']
                                ),
                            )
                        case _:
                            raise ClientError(
                                'Unable to parse metrics because of not managed model type'
                            ) from None
            except KeyError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e
            else:
                return job_status, None

        match self.__status:
            case JobStatus.ERROR:
                self.__model_metrics = None
            case JobStatus.MISSING_CURRENT:
                self.__model_metrics = None
            case JobStatus.SUCCEEDED:
                if self.__model_metrics is None:
                    _, metrics = invoke(
                        method='GET',
                        url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/model-quality',
                        valid_response_code=200,
                        func=__callback,
                    )
                    self.__model_metrics = metrics
            case JobStatus.IMPORTING:
                status, metrics = invoke(
                    method='GET',
                    url=f'{self.__base_url}/api/models/{str(self.__model_uuid)}/current/{str(self.__uuid)}/model-quality',
                    valid_response_code=200,
                    func=__callback,
                )
                self.__status = status
                self.__model_metrics = metrics

        return self.__model_metrics
