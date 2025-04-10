from typing import List, Optional
from urllib.parse import urlencode
from uuid import UUID

from pydantic import ValidationError
import requests

from radicalbit_platform_sdk.apis.tracing_root_trace import TracingRootTrace
from radicalbit_platform_sdk.apis.tracing_session import TracingSession
from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import ProjectDefinition, Session, Trace


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
