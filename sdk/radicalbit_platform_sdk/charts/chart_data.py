from typing import List, Optional

from pydantic import BaseModel


class ChartData(BaseModel):
    series_data: List[int]
    x_axis_data: List[str]

class NumericalBarChartData(BaseModel):
    title: str
    bucket_data: List[str]
    reference_data: List[float]
    current_data: Optional[List[float]] = None

class ConfusionMatrixChartData(BaseModel):
    axis_label: List[str]
    matrix: List[List[float]]
    color: Optional[List[str]] = ["#FFFFFF","#9B99A1"]
