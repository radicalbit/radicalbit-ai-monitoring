from typing import List, Optional

from pydantic import BaseModel

class MultiClassificationDistributionData(BaseModel):
    percentage: float
    count: float
    value: float

class MultiClassificationDistributionChartData(BaseModel):
    title: str
    x_axis_label: List[str]
    reference_data: List[MultiClassificationDistributionData]
    current_data: Optional[List[MultiClassificationDistributionData]] = None

class MultiClassificationLinearData(BaseModel):
    name: str
    values: List[List[str]]


class MultiClassificationLinearChartData(BaseModel):
    title: str
    reference_data: List[MultiClassificationLinearData]
    current_data: List[MultiClassificationLinearData]



 