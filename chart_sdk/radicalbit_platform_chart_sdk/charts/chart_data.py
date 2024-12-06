from typing import List
from pydantic import BaseModel

class ChartData(BaseModel):
    series_data: List[int]
    x_axis_data: List[str]