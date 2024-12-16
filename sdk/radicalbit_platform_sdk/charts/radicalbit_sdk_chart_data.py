from typing import List, Optional
from pydantic import BaseModel


from radicalbit_platform_sdk.models.dataset_data_quality import DataQuality
from radicalbit_platform_sdk.models.model_definition import BaseModelDefinition

class RbitBinaryDistributionData(BaseModel):
    title: str
    reference_data: DataQuality
    current_data: Optional[DataQuality] = None

class RbitDistributionData(BaseModel):
    model:BaseModelDefinition
    reference_data: DataQuality
    current_data: Optional[DataQuality] = None   