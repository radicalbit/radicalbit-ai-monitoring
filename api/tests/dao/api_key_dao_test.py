from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.project_dao import ProjectDAO
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
