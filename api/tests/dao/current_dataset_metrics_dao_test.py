from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.model_dao import ModelDAO
from tests.commons.db_integration import DatabaseIntegration
from tests.commons.db_mock import (
    get_sample_current_dataset,
    get_sample_current_metrics,
    get_sample_model,
)


class CurrentDatasetMetricsDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_dao = ModelDAO(cls.db)
        cls.metrics_dao = CurrentDatasetMetricsDAO(cls.db)
        cls.dataset_dao = CurrentDatasetDAO(cls.db)

    def test_insert_reference_dataset_metrics(self):
        self.model_dao.insert(get_sample_model())
        current = get_sample_current_dataset()
        self.dataset_dao.insert_current_dataset(current)
        metrics = get_sample_current_metrics(current_uuid=current.uuid)
        inserted = self.metrics_dao.insert_current_dataset_metrics(metrics)
        assert inserted == metrics

    def test_get_current_metrics_by_model_uuid(self):
        self.model_dao.insert(get_sample_model())
        current = get_sample_current_dataset()
        self.dataset_dao.insert_current_dataset(current)
        metrics = get_sample_current_metrics(current_uuid=current.uuid)
        self.metrics_dao.insert_current_dataset_metrics(metrics)
        retrieved = self.metrics_dao.get_current_metrics_by_model_uuid(
            model_uuid=current.model_uuid, current_uuid=current.uuid
        )
        assert retrieved.uuid == metrics.uuid
