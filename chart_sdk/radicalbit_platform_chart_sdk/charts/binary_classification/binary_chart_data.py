from typing import Optional, List
from pydantic import BaseModel,ConfigDict
from pydantic.alias_generators import to_camel

class Binary_Data(BaseModel):
    percentage: float
    count: float
    value: float

class BinaryChartData(BaseModel):
    title: str
    reference_data: List[Binary_Data]
    current_data: Optional[List[Binary_Data]] = None
