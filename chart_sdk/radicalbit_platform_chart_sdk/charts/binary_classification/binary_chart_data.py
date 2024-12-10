from typing import List, Optional

from pydantic import BaseModel


class Binary_Data(BaseModel):
    percentage: float
    count: float
    value: float

class BinaryChartData(BaseModel):
    title: str
    reference_data: List[Binary_Data]
    current_data: Optional[List[Binary_Data]] = None
