import unittest
from unittest.mock import MagicMock

from fastapi_pagination import Page, Params
import pytest
from sqlalchemy.exc import IntegrityError

from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.project_dao import ProjectDAO
from app.models.commons.order_type import OrderType
from app.models.exceptions import ExistingApiKeyError
from app.models.traces.api_key_dto import ApiKeyOut
from app.services.api_key_security import ApiKeySecurity
from app.services.api_key_service import ApiKeyService
from tests.commons import db_mock
from tests.services.project_service_test import project_uuid


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
            api_key=api_key,
            plain_api_key=api_key_sec.plain_key,
            project_uuid=project_uuid,
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

    def test_get_all(self):
        api_keys = [
            db_mock.get_sample_api_key(name='api_key'),
            db_mock.get_sample_api_key(name='api_key_one'),
            db_mock.get_sample_api_key(name='api_key_two'),
        ]
        self.api_key_dao.get_all = MagicMock(return_value=api_keys)
        res = self.api_key_service.get_all(project_uuid=db_mock.PROJECT_UUID)
        self.api_key_dao.get_all.assert_called_once_with(
            project_uuid=db_mock.PROJECT_UUID
        )
        assert len(res) == 3
        assert all(i.api_key is not None for i in res)

    def test_get_all_paginated(self):
        api_keys = [
            db_mock.get_sample_api_key(name='api_key'),
            db_mock.get_sample_api_key(name='api_key_one'),
            db_mock.get_sample_api_key(name='api_key_two'),
        ]
        page = Page.create(
            items=api_keys,
            total=len(api_keys),
            params=Params(page=1, size=10),
            order=OrderType.ASC,
            sort=None,
        )
        self.api_key_dao.get_all_paginated = MagicMock(return_value=page)
        res = self.api_key_service.get_all_paginated(project_uuid=db_mock.PROJECT_UUID)
        self.api_key_dao.get_all_paginated.assert_called_once_with(
            project_uuid=db_mock.PROJECT_UUID,
            params=Params(page=1, size=50),
            order=OrderType.ASC,
            sort=None,
        )
        assert len(res.items) == 3
        assert res.items[0].name == 'api_key'
        assert res.items[1].name == 'api_key_one'
        assert res.items[2].name == 'api_key_two'
