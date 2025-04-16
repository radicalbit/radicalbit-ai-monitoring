from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_embeddings_metrics_dao import (
    ReferenceDatasetEmbeddingsMetricsDAO,
)
from tests.commons.db_integration import DatabaseIntegration
from tests.commons.db_mock import (
    get_sample_model,
    get_sample_reference_dataset,
    get_sample_reference_embeddings_metrics,
)


class ReferenceDatasetEmbeddingsMetricsDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_dao = ModelDAO(cls.db)
        cls.metrics_dao = ReferenceDatasetEmbeddingsMetricsDAO(cls.db)
        cls.f_reference_dataset_dao = ReferenceDatasetDAO(cls.db)

    def test_insert_reference_dataset_embeddings_metrics(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_embeddings_metrics(
            reference_uuid=reference_upload.uuid
        )
        inserted = self.metrics_dao.insert_reference_embeddings_metrics(
            reference_metrics
        )
        assert inserted == reference_metrics

    def test_get_reference_embeddings_metrics_by_model_uuid(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_embeddings_metrics(
            reference_uuid=reference_upload.uuid
        )
        self.metrics_dao.insert_reference_embeddings_metrics(reference_metrics)
        retrieved = self.metrics_dao.get_reference_embeddings_metrics_by_model_uuid(
            model_uuid=reference_upload.model_uuid
        )
        assert retrieved.uuid == reference_metrics.uuid
