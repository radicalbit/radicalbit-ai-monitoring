from typing import Dict, List

from pyspark.sql import SparkSession, DataFrame

from metrics.chi2 import Chi2Test
from metrics.hellinger_distance import HellingerDistance
from metrics.jensen_shannon_distance import JensenShannonDistance
from metrics.ks import KolmogorovSmirnovTest
from metrics.psi import PSI
from metrics.wasserstein_distance import WassersteinDistance
from utils.drift_detector import DriftDetector
from utils.models import ColumnDefinition, DriftAlgorithmType, FieldTypes


class FeatureDriftManager:
    def __init__(
        self,
        spark_session: SparkSession,
        reference_data: DataFrame,
        current_data: DataFrame,
        prefix_id: str,
    ):
        self.detectors: Dict[str, DriftDetector] = {}

        self._register_detector(
            DriftAlgorithmType.CHI2,
            Chi2Test(spark_session, reference_data, current_data, prefix_id),
        )
        self._register_detector(
            DriftAlgorithmType.KS,
            KolmogorovSmirnovTest(
                spark_session, reference_data, current_data, prefix_id
            ),
        )
        self._register_detector(
            DriftAlgorithmType.PSI,
            PSI(spark_session, reference_data, current_data, prefix_id),
        )
        self._register_detector(
            DriftAlgorithmType.HELLINGER,
            HellingerDistance(spark_session, reference_data, current_data, prefix_id),
        )
        self._register_detector(
            DriftAlgorithmType.JS,
            JensenShannonDistance(
                spark_session, reference_data, current_data, prefix_id
            ),
        )
        self._register_detector(
            DriftAlgorithmType.WASSERSTEIN,
            WassersteinDistance(spark_session, reference_data, current_data, prefix_id),
        )

    def _register_detector(
        self, name: DriftAlgorithmType, detector: DriftDetector
    ) -> None:
        self.detectors[name] = detector

    def compute_drift_for_all_features(
        self, features: list[ColumnDefinition]
    ) -> Dict[str, List[dict]]:
        results: Dict[str, List[dict]] = {"feature_metrics": []}
        for idx, feature in enumerate(features):
            feature_dict_to_append = {
                "feature_name": feature.name,
                "field_type": FieldTypes.categorical.value,
                "drift_calc": []
            }
            results["feature_metrics"].append(feature_dict_to_append)
            if feature.drift:
                for drift_method in feature.drift:
                    limit = drift_method.p_value or drift_method.threshold
                    drift_algorithm = drift_method.name
                    # maybe check if feature name exists both reference and current
                    detector = self.detectors[drift_algorithm]
                    result = detector.detect_drift(feature, limit)
                    results["feature_metrics"][idx]["drift_calc"].append(result)
        return results
