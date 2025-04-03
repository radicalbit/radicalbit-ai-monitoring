from uuid import UUID

from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.models import Session


class TracingSession:
    def __init__(self, base_url: str, project_uuid: UUID, session: Session) -> None:
        self.__base_url = base_url
        self.__project_uuid = project_uuid
        self.__uuid = session.session_uuid
        self.__traces = session.traces
        self.__duration_ms = session.duration_ms
        self.__completion_tokens = session.completion_tokens
        self.__prompt_tokens = session.prompt_tokens
        self.__total_tokens = session.total_tokens
        self.__number_of_errors = session.number_of_errors
        self.__created_at = session.created_at
        self.__latest_trace_ts = session.latest_trace_ts

    def uuid(self) -> UUID:
        return self.__uuid

    def traces(self) -> int:
        return self.__traces

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

    def latest_trace_ts(self) -> str:
        return self.__latest_trace_ts

    def delete_traces(self) -> None:
        """Delete all traces for the session."""
        invoke(
            method='DELETE',
            url=f'{self.__base_url}/api/traces/project/{self.__project_uuid}/session/{self.__uuid}',
            valid_response_code=204,
            func=lambda _: None,
        )
