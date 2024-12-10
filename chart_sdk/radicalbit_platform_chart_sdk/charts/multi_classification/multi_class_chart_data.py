from typing import List, Optional

from pydantic import BaseModel

class MultiClassificationData(BaseModel):
    percentage: float
    count: float
    value: float

class MultiClassificationChartData(BaseModel):
    title: str
    x_axis_label: List[str]
    reference_data: List[MultiClassificationData]
    current_data: Optional[List[MultiClassificationData]] = None
