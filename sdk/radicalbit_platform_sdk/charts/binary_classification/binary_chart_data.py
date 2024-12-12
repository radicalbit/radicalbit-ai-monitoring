from typing import List, Optional

from pydantic import BaseModel


class BinaryDistributionData(BaseModel):
    percentage: float
    count: float
    value: float


class BinaryDistributionChartData(BaseModel):
    title: str
    y_axis_label: List[str]
    reference_data: List[BinaryDistributionData]
    current_data: Optional[List[BinaryDistributionData]] = None


class BinaryLinearChartData(BaseModel):
    title: str
    reference_data: List[List[str]]
    current_data: List[List[str]]
