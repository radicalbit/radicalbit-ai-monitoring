from metrics.drift_factory_pattern import FeatureDriftManager
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from pyspark.sql import DataFrame, SparkSession
from utils.models import DriftAlgorithmType


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
            list(DriftAlgorithmType),
        )
        return drift_manager.compute_drift_for_all_features(
            reference_dataset.model.features
        )

    @staticmethod
    def calculate_embeddings_drift(
        spark_session: SparkSession,
        reference_dataset: DataFrame,
        current_dataset: DataFrame,
        prefix_id: str,
    ):
        algorithm = DriftAlgorithmType.JS
        drift_manager = FeatureDriftManager(
            spark_session, reference_dataset, current_dataset, prefix_id, [algorithm]
        )
        return drift_manager.compute_embeddings_drift(algorithm)
