import unittest

from fastapi.testclient import TestClient

from app import main
from tests.commons import csv_file_mock as csv


class TestInferSchemaRoute(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app, raise_server_exceptions=False)

    def test_infer_schema(self):
        file = csv.get_correct_sample_csv_file()
        response = self.client.post(
            '/api/schema/infer-schema',
            files={'data_file': (file.filename, file.file)},
        )
        assert response.status_code == 200

    def test_infer_schema_invalid_file(self):
        file = csv.get_uncorrect_sample_csv_file()
        response = self.client.post(
            '/api/schema/infer-schema', files={'data_file': ('', file.file)}
        )
        assert response.status_code == 422

    def test_infer_schema_no_file(self):
        response = self.client.post('/api/schema/infer-schema')
        assert response.status_code == 422

    def test_infer_schema_empty_file(self):
        file = csv.get_empty_sample_csv_file()
        response = self.client.post(
            '/api/schema/infer-schema', files={'data_file': ('', file.file)}
        )
        assert response.status_code == 422
