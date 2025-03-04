from pyspark.sql import SparkSession
from metrics.drift_factory_pattern import FeatureDriftManager
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset


class DriftCalculator:
    @staticmethod
    def calculate_drift(
        spark_session: SparkSession,
        reference_dataset: ReferenceDataset,
        current_dataset: CurrentDataset,
        prefix_id: str,
    ):
        drift_manager = FeatureDriftManager(
            spark_session,
            reference_dataset.reference,
            current_dataset.current,
            prefix_id,
        )
        drift_results = drift_manager.compute_drift_for_all_features(
            reference_dataset.model.features
        )
        return drift_results
