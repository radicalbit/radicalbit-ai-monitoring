from typing import Optional
from pydantic import BaseModel, ConfigDict

from radicalbit_platform_sdk.apis.model import Model
from radicalbit_platform_sdk.apis.model_current_dataset import ModelCurrentDataset
from radicalbit_platform_sdk.apis.model_reference_dataset import ModelReferenceDataset

class RbitBinaryDistributionData(BaseModel):
    title: str
    reference: ModelReferenceDataset
    current: Optional[ModelCurrentDataset] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class RbitChartData(BaseModel):
    model: Model
    reference: ModelReferenceDataset
    current: Optional[ModelCurrentDataset] = None  

    model_config = ConfigDict(arbitrary_types_allowed=True)

class RbitChartResidualData(BaseModel):
    model: Model
    reference: Optional[ModelReferenceDataset] = None
    current: Optional[ModelCurrentDataset] = None  

    model_config = ConfigDict(arbitrary_types_allowed=True)

class RbitChartLinearData(BaseModel):
    model: Model
    reference: ModelReferenceDataset
    current: ModelCurrentDataset

    model_config = ConfigDict(arbitrary_types_allowed=True)