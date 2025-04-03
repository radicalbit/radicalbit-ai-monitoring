from typing import List, Optional
from urllib.parse import urlencode
from uuid import UUID

from pydantic import ValidationError
import requests

from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import ClientError
from radicalbit_platform_sdk.models import (
    LatenciesWidget,
    SessionsTraces,
    TraceTimeseries,
)


class TracingDashboard:
    def __init__(self, base_url: str, project_uuid: UUID) -> None:
        self.__project_uuid = project_uuid
        self.__base_url = (
            f'{base_url}/api/traces/dashboard/project/{str(self.__project_uuid)}'
        )

    def get_latencies_quantiles_for_root_traces(
        self, from_timestamp: int, to_timestamp: int
    ) -> Optional[LatenciesWidget]:
        params = {
            'fromTimestamp': from_timestamp,
            'toTimestamp': to_timestamp,
        }
        query_string = urlencode(params)
        url = f'{self.__base_url}/root_latencies?{query_string}'
        if requests.get(url).status_code == 204:
            return None

        def __callback(response: requests.Response) -> LatenciesWidget:
            try:
                return LatenciesWidget.model_validate(response.json())
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def get_latencies_quantiles_for_root_traces_by_session_uuid(
        self, from_timestamp: int, to_timestamp: int
    ) -> List[LatenciesWidget]:
        params = {
            'fromTimestamp': from_timestamp,
            'toTimestamp': to_timestamp,
        }
        query_string = urlencode(params)
        url = f'{self.__base_url}/root_latencies_session?{query_string}'

        def __callback(response: requests.Response) -> List[LatenciesWidget]:
            try:
                latencies_widgets = response.json()
                return [
                    LatenciesWidget.model_validate(widget)
                    for widget in latencies_widgets
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def get_latencies_quantiles_for_span_leaf(
        self, from_timestamp: int, to_timestamp: int
    ) -> List[LatenciesWidget]:
        params = {
            'fromTimestamp': from_timestamp,
            'toTimestamp': to_timestamp,
        }
        query_string = urlencode(params)
        url = f'{self.__base_url}/leaf_latencies?{query_string}'

        def __callback(response: requests.Response) -> List[LatenciesWidget]:
            try:
                latencies_widgets = response.json()
                return [
                    LatenciesWidget.model_validate(widget)
                    for widget in latencies_widgets
                ]
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def get_traces_by_time(
        self, from_timestamp: int, to_timestamp: int
    ) -> Optional[TraceTimeseries]:
        params = {
            'fromTimestamp': from_timestamp,
            'toTimestamp': to_timestamp,
        }
        query_string = urlencode(params)
        url = f'{self.__base_url}/trace_by_time?{query_string}'
        if requests.get(url).status_code == 204:
            return None

        def __callback(response: requests.Response) -> TraceTimeseries:
            try:
                return TraceTimeseries.model_validate(response.json())
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )

    def get_sessions_traces(
        self, from_timestamp: int, to_timestamp: int
    ) -> Optional[SessionsTraces]:
        params = {
            'fromTimestamp': from_timestamp,
            'toTimestamp': to_timestamp,
        }
        query_string = urlencode(params)
        url = f'{self.__base_url}/traces-by-session?{query_string}'
        if requests.get(url).status_code == 204:
            return None

        def __callback(response: requests.Response) -> SessionsTraces:
            try:
                return SessionsTraces.model_validate(response.json())
            except ValidationError as e:
                raise ClientError(f'Unable to parse response: {response.text}') from e

        return invoke(
            method='GET',
            url=url,
            valid_response_code=200,
            func=__callback,
        )
