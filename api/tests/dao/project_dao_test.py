from app.db.dao.project_dao import ProjectDAO
from tests.commons import db_mock
from tests.commons.db_integration import DatabaseIntegration


class ProjectDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_dao = ProjectDAO(cls.db)

    def test_insert(self):
        project = db_mock.get_sample_project()
        inserted = self.project_dao.insert(project)
        assert inserted.uuid == project.uuid
