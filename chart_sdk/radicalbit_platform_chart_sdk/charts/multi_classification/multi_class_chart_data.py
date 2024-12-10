from typing import Optional, List
from pydantic import BaseModel

class MultiClassificationData(BaseModel):
    percentage: float
    count: float
    value: float

class MultiClasssificationChartData(BaseModel):
    title: str
    reference_data: List[MultiClassificationData]
    current_data: Optional[List[MultiClassificationData]] = None
