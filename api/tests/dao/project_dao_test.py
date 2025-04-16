import uuid

from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.project_dao import ProjectDAO
from app.models.commons.order_type import OrderType
from tests.commons import db_mock
from tests.commons.db_integration import DatabaseIntegration


class ProjectDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_dao = ProjectDAO(cls.db)
        cls.api_key_dao = ApiKeyDAO(cls.db)

    def test_insert(self):
        project = db_mock.get_sample_project()
        inserted = self.project_dao.insert(project)
        assert inserted.uuid == project.uuid
        assert len(inserted.api_keys) == 1

    def test_get_by_uuid(self):
        project = db_mock.get_sample_project()
        self.project_dao.insert(project)
        retrieved = self.project_dao.get_by_uuid(project.uuid)
        assert retrieved.uuid == project.uuid

    def test_get_all_paginated(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')
        self.project_dao.insert(project1)
        self.project_dao.insert(project2)
        self.project_dao.insert(project3)

        projects = self.project_dao.get_all_paginated()
        assert projects.items[0].uuid == project1.uuid
        assert len(projects.items) == 3

    def test_get_all_paginated_ordered(self):
        project1 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project1')
        project2 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project2')
        project3 = db_mock.get_sample_project(uuid=uuid.uuid4(), name='project3')
        self.project_dao.insert(project1)
        self.project_dao.insert(project2)
        self.project_dao.insert(project3)

        projects = self.project_dao.get_all_paginated(order=OrderType.DESC, sort='name')
        assert projects.items[0].name == project3.name
        assert len(projects.items) == 3

    def test_update(self):
        project = db_mock.get_sample_project()
        api_key = db_mock.get_sample_api_key(name='api_key')
        self.project_dao.insert(project)
        self.api_key_dao.insert(api_key)
        inserted = self.project_dao.get_by_uuid(project.uuid)
        inserted.name = 'new_name_project'
        rows = self.project_dao.update(inserted)
        retrieved = self.project_dao.get_by_uuid(project.uuid)
        assert rows == 1
        assert retrieved.name == 'new_name_project'

    def test_delete(self):
        project = db_mock.get_sample_project()
        api_key = db_mock.get_sample_api_key(name='api_key')
        self.project_dao.insert(project)
        self.api_key_dao.insert(api_key)
        rows = self.project_dao.delete(project.uuid)
        retrieved = self.project_dao.get_by_uuid(project.uuid)
        api_key_retrieved = self.api_key_dao.get_all(db_mock.PROJECT_UUID)
        assert api_key_retrieved == []
        assert rows == 1
        assert retrieved is None
