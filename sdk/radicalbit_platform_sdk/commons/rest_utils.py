from typing import Callable

import requests

from radicalbit_platform_sdk.errors import (
    APIError,
    NetworkError,
    ServerError,
    UnhandledResponseCode,
)


def invoke(
    method: str, url: str, valid_response_code: int, func: Callable, data: any = None
):
    try:
        response = requests.request(method=method, url=url, data=data)
    except requests.RequestException as e:
        raise NetworkError(
            f'Network error: {{"method": "{method}", "url": "{url}", "exception": "{e}"}}'
        ) from e
    match response.status_code:
        case code if 500 <= code <= 599:
            raise ServerError(
                f'Server Error: {{"method": "{method}", "url": "{url}", "status_code": "{response.status_code}", "response": "{response.text}"}}'
            ) from None
        case code if 400 <= code <= 499:
            raise APIError(
                f'API Error: {{"method": "{method}", "url": "{url}", "status_code": "{response.status_code}", "response": "{response.text}"}}'
            ) from None
        case code if code == valid_response_code:
            return func(response)
        case _:
            raise UnhandledResponseCode(
                f'Unhandled Response Code Error: {{"method": "{method}", "url": "{url}", "status_code": "{response.status_code}", "response": "{response.text}"}}'
            ) from None
