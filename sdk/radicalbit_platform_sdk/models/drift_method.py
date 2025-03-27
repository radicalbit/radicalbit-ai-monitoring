from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from radicalbit_platform_sdk.models.drift_algorithm_type import DriftAlgorithmType
from radicalbit_platform_sdk.models.field_type import FieldType


class DriftMethod(BaseModel):
    name: DriftAlgorithmType
    threshold: Optional[float] = None
    p_value: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class ModelDriftMethod:
    def __init__(self, field_type: FieldType) -> None:
        self.__field_type = field_type
        self.__drift_methods = self._compliant_drift_methods()

    def _compliant_drift_methods(self) -> List[DriftMethod]:
        drift_mapping = {
            FieldType.categorical: [
                DriftMethod(name=DriftAlgorithmType.CHI2, p_value=0.05),
                DriftMethod(name=DriftAlgorithmType.HELLINGER, threshold=0.1),
                DriftMethod(name=DriftAlgorithmType.JS, threshold=0.1),
                DriftMethod(name=DriftAlgorithmType.KL, threshold=0.1),
            ],
            FieldType.numerical: [
                DriftMethod(name=DriftAlgorithmType.HELLINGER, threshold=0.1),
                DriftMethod(name=DriftAlgorithmType.WASSERSTEIN, threshold=0.1),
                DriftMethod(name=DriftAlgorithmType.KS, p_value=0.05),
                DriftMethod(name=DriftAlgorithmType.PSI, threshold=0.1),
                DriftMethod(name=DriftAlgorithmType.JS, threshold=0.1),
                DriftMethod(name=DriftAlgorithmType.KL, threshold=0.1),
            ],
            FieldType.datetime: [],
        }

        return drift_mapping.get(self.__field_type, [])

    def add_drift_method(self, method: DriftMethod) -> None:
        if method not in self.__drift_methods:
            self.__drift_methods.append(method)

    def remove_drift_method(self, method_name: DriftAlgorithmType) -> None:
        self.__drift_methods = [
            method for method in self.__drift_methods if method.name != method_name
        ]

    def get_drift_methods(self) -> List[DriftMethod]:
        return self.__drift_methods
