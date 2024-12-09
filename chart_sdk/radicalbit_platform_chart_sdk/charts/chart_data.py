from typing import Optional, List
from pydantic import BaseModel


class ChartData(BaseModel):
    series_data: List[int]
    x_axis_data: List[str]

class NumericalBarChartData(BaseModel):
    reference_data: List[float]
    current_data: Optional[List[float]]