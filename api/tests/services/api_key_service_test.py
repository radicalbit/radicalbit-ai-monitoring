import unittest
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.project_dao import ProjectDAO
from app.models.exceptions import ExistingApiKeyError
from app.models.traces.api_key_dto import ApiKeyOut
from app.services.api_key_security import ApiKeySecurity
from app.services.api_key_service import ApiKeyService
from tests.commons import db_mock


class ApiKeyServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_key_dao: ApiKeyDAO = MagicMock(spec_set=ApiKeyDAO)
        cls.project_dao: ProjectDAO = MagicMock(spec_set=ProjectDAO)
        cls.api_key_security: ApiKeySecurity = MagicMock(spec_set=ApiKeySecurity)
        cls.api_key_service = ApiKeyService(
            api_key_dao=cls.api_key_dao,
            project_dao=cls.project_dao,
            api_key_security=cls.api_key_security,
        )
        cls.mocks = [
            cls.api_key_dao,
            cls.api_key_security,
        ]

    def test_create_api_key_ok(self):
        api_key = db_mock.get_sample_api_key(name='new_api_key')
        api_key_sec = db_mock.get_sample_api_key_sec()
        self.api_key_dao.insert = MagicMock(return_value=api_key)
        self.api_key_security.generate_key = MagicMock(return_value=api_key_sec)
        api_key_in = db_mock.get_sample_api_key_in()
        res = self.api_key_service.create_api_key(db_mock.PROJECT_UUID, api_key_in)
        self.api_key_dao.insert.assert_called_once()
        assert res == ApiKeyOut.from_api_key(
            api_key=api_key, plain_api_key=api_key_sec.plain_key
        )

    def test_create_api_key_existing(self):
        api_key_sec = db_mock.get_sample_api_key_sec()
        self.api_key_security.generate_key = MagicMock(return_value=api_key_sec)
        self.api_key_dao.insert = MagicMock()
        self.api_key_dao.insert.side_effect = IntegrityError(
            None, None, BaseException()
        )
        api_key_in = db_mock.get_sample_api_key_in()
        pytest.raises(
            ExistingApiKeyError,
            self.api_key_service.create_api_key,
            db_mock.PROJECT_UUID,
            api_key_in,
        )
