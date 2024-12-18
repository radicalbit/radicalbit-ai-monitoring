from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.completion_dataset_metrics_dao import CompletionDatasetMetricsDAO
from app.db.dao.model_dao import ModelDAO
from app.models.model_dto import ModelType
from tests.commons.db_integration import DatabaseIntegration
from tests.commons.db_mock import (
    get_sample_completion_dataset,
    get_sample_completion_metrics,
    get_sample_model,
)


class CompletionDatasetMetricsDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_dao = ModelDAO(cls.db)
        cls.metrics_dao = CompletionDatasetMetricsDAO(cls.db)
        cls.f_completion_dataset_dao = CompletionDatasetDAO(cls.db)

    def test_insert_completion_dataset_metrics(self):
        self.model_dao.insert(
            get_sample_model(
                model_type=ModelType.TEXT_GENERATION,
                features=None,
                target=None,
                outputs=None,
                timestamp=None,
            )
        )
        completion_upload = get_sample_completion_dataset()
        self.f_completion_dataset_dao.insert_completion_dataset(completion_upload)
        completion_metrics = get_sample_completion_metrics(
            completion_uuid=completion_upload.uuid
        )
        inserted = self.metrics_dao.insert_completion_metrics(completion_metrics)
        assert inserted == completion_metrics

    def test_get_completion_metrics_by_model_uuid(self):
        self.model_dao.insert(
            get_sample_model(
                model_type=ModelType.TEXT_GENERATION,
                features=None,
                target=None,
                outputs=None,
                timestamp=None,
            )
        )
        completion = get_sample_completion_dataset()
        self.f_completion_dataset_dao.insert_completion_dataset(completion)
        metrics = get_sample_completion_metrics()
        self.metrics_dao.insert_completion_metrics(metrics)
        retrieved = self.metrics_dao.get_completion_metrics_by_model_uuid(
            model_uuid=completion.model_uuid, completion_uuid=completion.uuid
        )
        assert retrieved.uuid == metrics.uuid
