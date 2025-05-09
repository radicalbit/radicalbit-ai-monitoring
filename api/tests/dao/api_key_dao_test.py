from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.project_dao import ProjectDAO
from app.db.tables.api_key_table import ApiKey
from tests.commons import db_mock
from tests.commons.db_integration import DatabaseIntegration


class ApiKeyDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_key_dao = ApiKeyDAO(cls.db)
        cls.project_dao = ProjectDAO(cls.db)

    def test_insert(self):
        api_key = db_mock.get_sample_api_key(name='new_api_key')
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        inserted = self.api_key_dao.insert(api_key)
        assert inserted.project_uuid == api_key.project_uuid
        assert inserted.name == api_key.name

    def test_get_all(self):
        api_keys = [
            db_mock.get_sample_api_key(name='api_key'),
            db_mock.get_sample_api_key(name='api_key_one'),
            db_mock.get_sample_api_key(name='api_key_two'),
        ]
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        _ = [self.api_key_dao.insert(i) for i in api_keys]
        res = self.api_key_dao.get_all(db_mock.PROJECT_UUID)
        assert len(res) == 4

    def test_get_all_paginated(self):
        api_keys = [
            db_mock.get_sample_api_key(name='api_key'),
            db_mock.get_sample_api_key(name='api_key_one'),
            db_mock.get_sample_api_key(name='api_key_two'),
        ]
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        _ = [self.api_key_dao.insert(i) for i in api_keys]
        res = self.api_key_dao.get_all_paginated(db_mock.PROJECT_UUID)
        assert len(res.items) == 4

    def test_get_all_paginated_ordered(self):
        api_keys = [
            db_mock.get_sample_api_key(name='aaa'),
            db_mock.get_sample_api_key(name='bbb'),
            db_mock.get_sample_api_key(name='ccc'),
        ]
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        _ = [self.api_key_dao.insert(i) for i in api_keys]
        res = self.api_key_dao.get_all_paginated(db_mock.PROJECT_UUID, sort='name')
        assert len(res.items) == 4
        assert res.items[0].name == 'aaa'

    def test_get_api_key(self):
        api_key = db_mock.get_sample_api_key(name='aaa')
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        self.api_key_dao.insert(api_key)
        res = self.api_key_dao.get_api_key(db_mock.PROJECT_UUID, 'aaa')
        assert isinstance(res, ApiKey)
        assert res.name == api_key.name
        assert res.project_uuid == api_key.project_uuid

    def test_get_by_hashed_key_ok(self):
        api_key = db_mock.get_sample_api_key(name='new_api_key')
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        self.api_key_dao.insert(api_key)
        res = self.api_key_dao.get_by_hashed_key(api_key.hashed_key)
        assert res.hashed_key == api_key.hashed_key

    def test_get_by_hashed_key_none(self):
        api_key = db_mock.get_sample_api_key(name='new_api_key')
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        self.api_key_dao.insert(api_key)
        res = self.api_key_dao.get_by_hashed_key('hashed new key')
        assert res is None

    def test_delete_api_key(self):
        api_key = db_mock.get_sample_api_key(name='aaa')
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        self.api_key_dao.insert(api_key)
        res = self.api_key_dao.delete_api_key(db_mock.PROJECT_UUID, 'aaa')
        assert res == 1

    def test_delete_last_key(self):
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        res = self.api_key_dao.delete_api_key(db_mock.PROJECT_UUID, 'default')
        assert res == 0
