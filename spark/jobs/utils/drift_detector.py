from abc import ABC, abstractmethod

from utils.models import ColumnDefinition, FieldTypes


class DriftDetector(ABC):
    @abstractmethod
    def detect_drift(self, feature: ColumnDefinition, **kwargs) -> dict:
        pass

    @property
    @abstractmethod
    def supported_feature_types(self) -> list[FieldTypes]:
        pass
