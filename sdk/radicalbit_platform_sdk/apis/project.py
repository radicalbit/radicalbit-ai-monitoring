from typing import List, Optional
from urllib.parse import urlencode
from uuid import UUID

from pydantic import TypeAdapter, ValidationError
import requests

from radicalbit_platform_sdk.apis.api_key import ApiKey
from radicalbit_platform_sdk.apis.tracing_root_trace import TracingRootTrace
from radicalbit_platform_sdk.apis.tracing_session import TracingSession
from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    ApiKeyDefinition,
    CreateApiKey,
    ProjectDefinition,
    Session,
    Trace,
)


class Project:
    def __init__(self, base_url: str, definition: ProjectDefinition) -> None:
        self.__uuid = definition.uuid
        self.__base_url = base_url
        self.__name = definition.name

    @property
    def uuid(self) -> UUID:
        return self.__uuid

    @property
    def name(self) -> str:
        return self.__name

    def delete(self) -> None:
        """Delete the actual `Project` from the platform

        :return: None
        """
        invoke(
            method='DELETE',
            url=f'{self.__base_url}/api/projects/{self.__uuid}',
            valid_response_code=200,
            func=lambda _: None,
        )

    def get_all_sessions(self) -> List[TracingSession]:
        """Fetch all sessions for the project."""

        def __callback(response: requests.Response) -> List[TracingSession]:
            try:
                sessions = response.json()
                return [
                    TracingSession(self.__base_url, self.__uuid, Session(**session))
                    for session in sessions
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/traces/project/{self.__uuid}/session/all',
            valid_response_code=200,
            func=__callback,
        )

    def get_all_root_traces(
        self,
        trace_id: Optional[str] = None,
        session_uuid: Optional[UUID] = None,
        from_timestamp: Optional[int] = None,
        to_timestamp: Optional[int] = None,
    ) -> List[TracingRootTrace]:
        """Fetch all root traces for the project."""
        params = {
            k: v
            for k, v in {
                'traceId': trace_id,
                'sessionUuid': session_uuid,
                'fromTimestamp': from_timestamp,
                'toTimestamp': to_timestamp,
            }.items()
            if v is not None
        }
        query_string = urlencode(params)
        url = f'{self.__base_url}/api/traces/project/{self.__uuid}/trace/all?{query_string}'

        def __callback(response: requests.Response) -> List[TracingRootTrace]:
            try:
                root_traces = response.json()
                return [
                    TracingRootTrace(self.__base_url, self.__uuid, Trace(**trace))
                    for trace in root_traces
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def create_api_key(self, api_key: CreateApiKey) -> ApiKey:
        def __callback(response: requests.Response) -> ApiKey:
            try:
                response_api_key = ApiKeyDefinition.model_validate(response.json())
                return ApiKey(self.__base_url, response_api_key)
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='POST',
            url=f'{self.__base_url}/api/api-key/project/{str(self.uuid)}',
            valid_response_code=201,
            func=__callback,
            data=api_key.model_dump_json(),
        )

    def get_api_key(self, name: str) -> ApiKey:
        def __callback(response: requests.Response) -> ApiKey:
            try:
                response_api_key = ApiKeyDefinition.model_validate(response.json())
                return ApiKey(self.__base_url, response_api_key)
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/api-key/project/{str(self.uuid)}/api-keys/{name}',
            valid_response_code=200,
            func=__callback,
        )

    def search_api_keys(self) -> List[ApiKey]:
        def __callback(response: requests.Response) -> List[ApiKey]:
            try:
                adapter = TypeAdapter(List[ApiKeyDefinition])
                api_keys_definitions = adapter.validate_python(response.json())
                return [
                    ApiKey(self.__base_url, api_key) for api_key in api_keys_definitions
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=f'{self.__base_url}/api/api-key/project/{str(self.uuid)}/all',
            valid_response_code=200,
            func=__callback,
        )

    def delete_api_key(self, name: str) -> None:
        invoke(
            method='DELETE',
            url=f'{self.__base_url}/api/api-key/project/{self.uuid}/api-keys/{name}',
            valid_response_code=204,
            func=lambda _: None,
        )
