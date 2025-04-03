from typing import Optional
from uuid import UUID

from pydantic import ValidationError
import requests

from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import Span, Trace, TreeNode


class TracingRootTrace:
    def __init__(self, base_url: str, project_uuid: UUID, trace: Trace) -> None:
        self.__base_url = base_url
        self.__project_uuid = project_uuid
        self.__id = trace.trace_id
        self.__span_id = trace.span_id
        self.__session_uuid = trace.session_uuid
        self.__spans = trace.spans
        self.__duration_ms = trace.duration_ms
        self.__completion_tokens = trace.completion_tokens
        self.__prompt_tokens = trace.prompt_tokens
        self.__total_tokens = trace.total_tokens
        self.__number_of_errors = trace.number_of_errors
        self.__created_at = trace.created_at
        self.__tree = trace.tree

    def id(self) -> str:
        return self.__id

    def span_id(self) -> str:
        return self.__span_id

    def session_uuid(self) -> UUID:
        return self.__session_uuid

    def spans(self) -> int:
        return self.__spans

    def duration_ms(self) -> float:
        return self.__duration_ms

    def completion_tokens(self) -> int:
        return self.__completion_tokens

    def prompt_tokens(self) -> int:
        return self.__prompt_tokens

    def total_tokens(self) -> int:
        return self.__total_tokens

    def errors(self) -> int:
        return self.__number_of_errors

    def created_at(self) -> str:
        return self.__created_at

    def tree_node(self) -> Optional[TreeNode]:
        return self.__tree

    def get_trace(self) -> Optional[Trace]:
        url = f'{self.__base_url}/api/traces/project/{self.__project_uuid}/trace/{self.__id}'
        if requests.get(url).status_code == 204:
            return None

        def __callback(response: requests.Response) -> Trace:
            try:
                return Trace.model_validate(response.json())
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def get_span(self) -> Optional[Span]:
        url = f'{self.__base_url}/api/traces/project/{self.__project_uuid}/trace/{self.__id}/span/{self.__span_id}'
        if requests.get(url).status_code == 204:
            return None

        def __callback(response: requests.Response) -> Span:
            try:
                return Span.model_validate(response.json())
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def delete_trace(self) -> None:
        """Delete trace"""
        invoke(
            method='DELETE',
            url=f'{self.__base_url}/api/traces/project/{self.__project_uuid}/trace/{self.__id}',
            valid_response_code=204,
            func=lambda _: None,
        )
