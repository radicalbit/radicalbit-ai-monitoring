from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from radicalbit_platform_sdk.apis.model_current_dataset import ModelCurrentDataset
from radicalbit_platform_sdk.apis.model_reference_dataset import ModelReferenceDataset
from radicalbit_platform_sdk.models.dataset_data_quality import ClassMetrics


class MultiClassificationDistributionData(BaseModel):
    percentage: float
    count: float
    value: float


class MultiClassificationDistributionChartData(BaseModel):
    title: str
    reference_data: List[ClassMetrics]
    current_data: Optional[List[ClassMetrics]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MultiClassificationLinearData(BaseModel):
    name: str
    values: List[List[str]]


class MultiClassificationLinearChartData(BaseModel):
    title: str
    reference_data: List[MultiClassificationLinearData]
    current_data: List[MultiClassificationLinearData]
