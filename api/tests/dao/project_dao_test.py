import uuid

from app.db.dao.project_dao import ProjectDAO
from app.models.dataset_dto import OrderType
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
