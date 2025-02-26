from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel
from pyspark.sql import SparkSession, DataFrame

from metrics.chi2 import Chi2Test
from metrics.ks import KolmogorovSmirnovTest
from metrics.psi import PSI
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from utils.models import FieldTypes, ColumnDefinition


class DriftAlgorithmType(str, Enum):
    HELLINGER = "hellinger"
    WASSERSTEIN = "wasserstein"
    KS = "ks"
    JS = "js"
    PSI = "psi"
    CHI2 = "chi2"

class DriftDetectionConfig(BaseModel):
    feature: str
    algorithm: DriftAlgorithmType
    field_type: FieldTypes
    threshold: Optional[float] = None
    p_value: Optional[float] = None

class DriftCalc(BaseModel):
    type: str
    value: float
    has_drift: bool

class DriftDetectionResult(BaseModel):
    feature_name: str
    field_type: float
    drift_calc: DriftCalc

class DriftDetector(ABC):

    @abstractmethod
    def detect_drift(self, feature: str) -> DriftDetectionResult:
        pass

    @property
    @abstractmethod
    def supported_feature_types(self) -> List[FieldTypes]:
        return [FieldTypes.numerical]

class FeatureDriftManager:
    def __init__(self, spark_session: SparkSession, reference_data: DataFrame, current_data: DataFrame, prefix_id: str):
        self.detectors: Dict[str, DriftDetector] = {}

        self._register_detector(DriftAlgorithmType.CHI2, Chi2Test(spark_session, reference_data, current_data, prefix_id))
        self._register_detector(DriftAlgorithmType.KS, KolmogorovSmirnovTest(spark_session, reference_data, current_data, prefix_id))
        self._register_detector(DriftAlgorithmType.PSI, PSI(spark_session, reference_data, current_data, prefix_id))

    def _register_detector(self, name: DriftAlgorithmType, detector: DriftDetector) -> None:
        self.detectors[name] = detector

    def compute_drift_for_all_features(
            self, features: list[ColumnDefinition]
    ) -> Dict[str, List[DriftDetectionResult]]:
        results: Dict[str, List[DriftDetectionResult]] = {}
        for feature in features:
            feature_name = feature.name
            drift_algorithm = feature.drift.name
            # maybe check if feature name exists both reference and current
            detector = self.detectors[drift_algorithm]
            result = detector.detect_drift(
                feature_name
            )
            results["feature_metrics"].append(result)
        return results