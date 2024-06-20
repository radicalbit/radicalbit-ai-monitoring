from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_metrics_dao import ReferenceDatasetMetricsDAO
from tests.commons.db_integration import DatabaseIntegration
from tests.commons.db_mock import (
    get_sample_model,
    get_sample_reference_dataset,
    get_sample_reference_metrics,
)


class ReferenceDatasetMetricsDAOTest(DatabaseIntegration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model_dao = ModelDAO(cls.db)
        cls.metrics_dao = ReferenceDatasetMetricsDAO(cls.db)
        cls.f_reference_dataset_dao = ReferenceDatasetDAO(cls.db)

    def test_insert_reference_dataset_metrics(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_metrics(
            reference_uuid=reference_upload.uuid
        )
        inserted = self.metrics_dao.insert_reference_metrics(reference_metrics)
        assert inserted == reference_metrics

    def test_get_reference_metrics_by_model_uuid(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_metrics(
            reference_uuid=reference_upload.uuid
        )
        self.metrics_dao.insert_reference_metrics(reference_metrics)
        retrieved = self.metrics_dao.get_reference_metrics_by_model_uuid(
            model_uuid=reference_upload.model_uuid
        )
        assert retrieved.uuid == reference_metrics.uuid

    def test_get_reference_metrics_by_file_uuid(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_metrics(
            reference_uuid=reference_upload.uuid
        )
        self.metrics_dao.insert_reference_metrics(reference_metrics)
        retrieved = self.metrics_dao.get_reference_metrics_by_reference_uuid(
            reference_uuid=reference_upload.uuid
        )
        assert retrieved.uuid == reference_metrics.uuid

    def test_update_reference_model_quality(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_metrics(
            reference_uuid=reference_upload.uuid
        )
        self.metrics_dao.insert_reference_metrics(reference_metrics)
        model_quality = {'accuracy': 0.1}
        self.metrics_dao.update_reference_model_quality(
            reference_metrics.reference_uuid, model_quality
        )
        retrieved = self.metrics_dao.get_reference_metrics_by_reference_uuid(
            reference_uuid=reference_upload.uuid
        )
        assert retrieved.model_quality == model_quality

    def test_update_reference_data_quality(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_metrics(
            reference_uuid=reference_upload.uuid
        )
        self.metrics_dao.insert_reference_metrics(reference_metrics)
        data_quality = {'avg': 0.1}
        self.metrics_dao.update_reference_data_quality(
            reference_metrics.reference_uuid, data_quality
        )
        retrieved = self.metrics_dao.get_reference_metrics_by_reference_uuid(
            reference_uuid=reference_upload.uuid
        )
        assert retrieved.data_quality == data_quality

    def test_update_reference_statistics(self):
        self.model_dao.insert(get_sample_model())
        reference_upload = get_sample_reference_dataset()
        self.f_reference_dataset_dao.insert_reference_dataset(reference_upload)
        reference_metrics = get_sample_reference_metrics(
            reference_uuid=reference_upload.uuid
        )
        self.metrics_dao.insert_reference_metrics(reference_metrics)
        statistics = {'duplicate_rows': 2}
        self.metrics_dao.update_reference_statistics(
            reference_metrics.reference_uuid, statistics
        )
        retrieved = self.metrics_dao.get_reference_metrics_by_reference_uuid(
            reference_uuid=reference_upload.uuid
        )
        assert retrieved.statistics == statistics
