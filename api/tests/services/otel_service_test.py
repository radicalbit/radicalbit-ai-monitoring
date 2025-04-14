import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import Response
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
)
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

    @patch.object(OtelService, '_inject_project_uuid', return_value=b'modified-body')
    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_traces_ok(self, mock_forward_to_collector, mock_inject):
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

        res = asyncio.run(
            self.otel_service.write_traces(api_key, b'original-body', headers)
        )
        assert res.content == mock_response.content

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_inject.assert_called_once_with(
            b'original-body', str(sample_api_key.project_uuid)
        )
        mock_forward_to_collector.assert_awaited_once_with(
            b'modified-body', headers, 'traces'
        )

    @patch.object(OtelService, '_inject_project_uuid', return_value=b'modified-body')
    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_metrics_ok(self, mock_forward_to_collector, mock_inject):
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

        res = asyncio.run(
            self.otel_service.write_metrics(api_key, b'original-body', headers)
        )
        assert res.content == mock_response.content

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_inject.assert_called_once_with(
            b'original-body', str(sample_api_key.project_uuid)
        )
        mock_forward_to_collector.assert_awaited_once_with(
            b'modified-body', headers, 'metrics'
        )

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

    @patch.object(OtelService, '_inject_project_uuid', return_value=b'modified-body')
    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_traces_collector_error(self, mock_forward_to_collector, mock_inject):
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        hashed_key = hash_key(api_key)
        sample_api_key = db_mock.get_sample_api_key(hashed_key=hashed_key)

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=sample_api_key)
        mock_forward_to_collector.side_effect = OtelInternalError('Request failed')

        with pytest.raises(OtelInternalError):
            asyncio.run(
                self.otel_service.write_traces(api_key, b'original-body', headers)
            )

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_inject.assert_called_once_with(
            b'original-body', str(sample_api_key.project_uuid)
        )
        mock_forward_to_collector.assert_awaited_once_with(
            b'modified-body', headers, 'traces'
        )

    @patch.object(OtelService, '_inject_project_uuid', return_value=b'modified-body')
    @patch.object(OtelService, '_forward_to_collector', new_callable=AsyncMock)
    def test_write_metrics_collector_error(
        self, mock_forward_to_collector, mock_inject
    ):
        api_key = 'valid-api-key'
        headers = {'Authorization': f'Bearer {api_key}'}

        hashed_key = hash_key(api_key)
        sample_api_key = db_mock.get_sample_api_key(hashed_key=hashed_key)

        self.api_key_dao.get_by_hashed_key = MagicMock(return_value=sample_api_key)
        mock_forward_to_collector.side_effect = OtelInternalError('Request failed')

        with pytest.raises(OtelInternalError):
            asyncio.run(
                self.otel_service.write_metrics(api_key, b'original-body', headers)
            )

        self.api_key_dao.get_by_hashed_key.assert_called_once()
        mock_inject.assert_called_once_with(
            b'original-body', str(sample_api_key.project_uuid)
        )
        mock_forward_to_collector.assert_awaited_once_with(
            b'modified-body', headers, 'metrics'
        )

    def test_inject_project_uuid_overwrites_service_name(self):
        request = ExportTraceServiceRequest()
        resource_span = request.resource_spans.add()
        resource = resource_span.resource
        attr = resource.attributes.add()
        attr.key = 'service.name'
        attr.value.string_value = 'original-service'

        body = request.SerializeToString()
        project_uuid = '123e4567-e89b-12d3-a456-426614174000'

        modified_body = self.otel_service._inject_project_uuid(body, project_uuid)

        modified_request = ExportTraceServiceRequest()
        modified_request.ParseFromString(modified_body)

        modified_service_name = None
        for attr in modified_request.resource_spans[0].resource.attributes:
            if attr.key == 'service.name':
                modified_service_name = attr.value.string_value

        assert modified_service_name == project_uuid
