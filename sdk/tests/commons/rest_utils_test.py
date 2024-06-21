import random
import unittest

import pytest
import requests
import responses

from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.errors import (
    APIError,
    NetworkError,
    ServerError,
    UnhandledResponseCode,
)


class RestUtilsTest(unittest.TestCase):
    @responses.activate
    def test_invoke_network_error(self):
        base_url = 'http://api:80'
        responses.add(method=responses.GET, url=f'{base_url}0/api', status=200)
        with pytest.raises(NetworkError):
            invoke('GET', f'{base_url}/api', 200, lambda resp: None)

    @responses.activate
    def test_invoke_server_error(self):
        base_url = 'http://api:9000'
        responses.add(
            method=responses.GET, url=f'{base_url}/api', status=random.randint(500, 599)
        )
        with pytest.raises(ServerError):
            invoke('GET', f'{base_url}/api', 200, lambda resp: None)

    @responses.activate
    def test_invoke_api_error(self):
        base_url = 'http://api:9000'
        responses.add(
            method=responses.GET, url=f'{base_url}/api', status=random.randint(400, 499)
        )
        with pytest.raises(APIError):
            invoke('GET', f'{base_url}/api', 200, lambda resp: None)

    @responses.activate
    def test_invoke_unhandled_response_code_error(self):
        base_url = 'http://api:9000'
        responses.add(
            method=responses.GET, url=f'{base_url}/api', status=random.randint(201, 299)
        )
        with pytest.raises(UnhandledResponseCode):
            invoke('GET', f'{base_url}/api', 200, lambda resp: None)

    @responses.activate
    def test_invoke_ok(self):
        base_url = 'http://api:9000'
        response_body = 'Hooray, it works'
        responses.add(
            method=responses.GET,
            url=f'{base_url}/api',
            body=response_body,
            status=200,
            content_type='text/plain',
        )

        def __callback(response: requests.Response):
            return response.text

        result = invoke('GET', f'{base_url}/api', 200, __callback)
        assert result == response_body
