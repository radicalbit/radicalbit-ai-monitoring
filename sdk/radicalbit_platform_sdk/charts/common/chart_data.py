from typing import List, Optional

from pydantic import BaseModel


class NumericalBarChartData(BaseModel):
    title: str
    bucket_data: List[float]
    reference_data: List[float]
    current_data: Optional[List[float]] = None


class ConfusionMatrixChartData(BaseModel):
    axis_label: List[str]
    matrix: List[List[float]]
    color: Optional[List[str]] = ['#FFFFFF', '#9B99A1']
