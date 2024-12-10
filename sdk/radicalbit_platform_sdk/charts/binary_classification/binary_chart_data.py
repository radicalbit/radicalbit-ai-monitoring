from typing import List, Optional

from pydantic import BaseModel


class Binary_Data(BaseModel):
    percentage: float
    count: float
    value: float

class BinaryChartData(BaseModel):
    title: str
    y_axis_label: List[str]
    reference_data: List[Binary_Data]
    current_data: Optional[List[Binary_Data]] = None
