import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import Response
import pytest

from app.db.dao.api_key_dao import ApiKeyDAO
from app.models.exceptions import OtelInternalError, OtelUnauthorizedError
from app.services.commons.keyed_hash_algorithm import hash_key
from app.services.otel_service import OtelService
from tests.commons import db_mock


class OtelServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_key_dao = MagicMock(spec_set=ApiKeyDAO)
        cls.otel_service = OtelService(
            api_key_dao=cls.api_key_dao,
        )
        cls.mocks = [
            cls.api_key_dao,
        ]

    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_traces_ok(self, mock_forward_to_collector):
        mock_response = Response(
            status_code=201,
            content=b'ok',
            headers={'content-type': 'application/json'},
        )
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        hashed_key = hash_key(api_key)
        sample_api_key = db_mock.get_sample_api_key(hashed_key=hashed_key)

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=sample_api_key)
        mock_forward_to_collector.return_value = mock_response

        res = asyncio.run(self.otel_service.write_traces(api_key, b'{}', headers))
        assert res.content == mock_response.content

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_forward_to_collector.assert_awaited_once()

    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_metrics_ok(self, mock_forward_to_collector):
        mock_response = Response(
            status_code=201,
            content=b'ok',
            headers={'content-type': 'application/json'},
        )
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        hashed_key = hash_key(api_key)
        sample_api_key = db_mock.get_sample_api_key(hashed_key=hashed_key)

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=sample_api_key)
        mock_forward_to_collector.return_value = mock_response

        res = asyncio.run(self.otel_service.write_metrics(api_key, b'{}', headers))
        assert res.content == mock_response.content

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_forward_to_collector.assert_awaited_once()

    def test_write_traces_api_key_not_found(self):
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=None)

        with pytest.raises(OtelUnauthorizedError):
            asyncio.run(self.otel_service.write_traces(api_key, b'{}', headers))

        self.api_key_dao.get_by_hashed_key.assert_called_once()

    def test_write_metrics_api_key_not_found(self):
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=None)

        with pytest.raises(OtelUnauthorizedError):
            asyncio.run(self.otel_service.write_metrics(api_key, b'{}', headers))

        self.api_key_dao.get_by_hashed_key.assert_called_once()

    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_traces_collector_error(self, mock_forward_to_collector):
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        hashed_key = hash_key(api_key)
        sample_api_key = db_mock.get_sample_api_key(hashed_key=hashed_key)

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=sample_api_key)
        mock_forward_to_collector.side_effect = OtelInternalError('Request failed')

        with pytest.raises(OtelInternalError):
            asyncio.run(self.otel_service.write_traces(api_key, b'{}', headers))

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_forward_to_collector.assert_awaited_once()

    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_metrics_collector_error(self, mock_forward_to_collector):
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        hashed_key = hash_key(api_key)
        sample_api_key = db_mock.get_sample_api_key(hashed_key=hashed_key)

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=sample_api_key)
        mock_forward_to_collector.side_effect = OtelInternalError('Request failed')

        with pytest.raises(OtelInternalError):
            asyncio.run(self.otel_service.write_metrics(api_key, b'{}', headers))

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_forward_to_collector.assert_awaited_once()
