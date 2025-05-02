from typing import Dict, List

from models.map_algo_class import MapDriftEnumToClass
from pyspark.sql import DataFrame, SparkSession
from utils.drift_detector import DriftDetector
from utils.models import (
    ColumnDefinition,
    DriftAlgorithmType,
    DriftMethod,
    FieldTypes,
    SupportedTypes,
)


class FeatureDriftManager:
    def __init__(
        self,
        spark_session: SparkSession,
        reference_data: DataFrame,
        current_data: DataFrame,
        prefix_id: str,
        algorithm_to_register: list[DriftAlgorithmType],
    ):
        self.detectors: Dict[str, DriftDetector] = {}

        for i in algorithm_to_register:
            DriftAlgoClass = MapDriftEnumToClass.get_calculator_class(i)
            self._register_detector(
                i,
                DriftAlgoClass(spark_session, reference_data, current_data, prefix_id),
            )

        # self._register_detector(
        #     DriftAlgorithmType.JS,
        #     JensenShannonDistance(
        #         spark_session, reference_data, current_data, prefix_id
        #     ),
        # )
        #
        # self._register_detector(
        #     DriftAlgorithmType.CHI2,
        #     Chi2Test(spark_session, reference_data, current_data, prefix_id),
        # )
        # self._register_detector(
        #     DriftAlgorithmType.KS,
        #     KolmogorovSmirnovTest(
        #         spark_session, reference_data, current_data, prefix_id
        #     ),
        # )
        # self._register_detector(
        #     DriftAlgorithmType.PSI,
        #     PSI(spark_session, reference_data, current_data, prefix_id),
        # )
        # self._register_detector(
        #     DriftAlgorithmType.HELLINGER,
        #     HellingerDistance(spark_session, reference_data, current_data, prefix_id),
        # )
        # self._register_detector(
        #     DriftAlgorithmType.WASSERSTEIN,
        #     WassersteinDistance(spark_session, reference_data, current_data, prefix_id),
        # )
        #
        # self._register_detector(
        #     DriftAlgorithmType.KL,
        #     KullbackLeiblerDivergence(
        #         spark_session, reference_data, current_data, prefix_id
        #     ),
        # )

    def _register_detector(
        self, name: DriftAlgorithmType, detector: DriftDetector
    ) -> None:
        self.detectors[name] = detector

    def compute_drift_for_all_features(
        self, features: list[ColumnDefinition]
    ) -> Dict[str, List[dict]]:
        results: Dict[str, List[dict]] = {'feature_metrics': []}
        for idx, feature in enumerate(features):
            feature_dict_to_append = {
                'feature_name': feature.name,
                'field_type': feature.field_type.value,
                'drift_calc': [],
            }
            results['feature_metrics'].append(feature_dict_to_append)
            if feature.drift:
                for drift_method in feature.drift:
                    params = {
                        'p_value': drift_method.p_value,
                        'threshold': drift_method.threshold,
                    }
                    drift_algorithm = drift_method.name
                    # TODO maybe check if feature name exists both reference and current
                    detector = self.detectors[drift_algorithm]
                    result = detector.detect_drift(feature, **params)
                    results['feature_metrics'][idx]['drift_calc'].append(result)
        return results

    def compute_embeddings_drift(self, algorithm: DriftAlgorithmType) -> float:
        drift_method = DriftMethod(name=algorithm, threshold=0.1)
        feature = ColumnDefinition(
            name='distance',
            type=SupportedTypes.int,
            field_type=FieldTypes.numerical,
            drift=[drift_method],
        )
        detector = self.detectors[drift_method.name]
        params = {
            'p_value': drift_method.p_value,
            'threshold': drift_method.threshold,
        }
        result = detector.detect_drift(feature, **params)
        return result['value']
