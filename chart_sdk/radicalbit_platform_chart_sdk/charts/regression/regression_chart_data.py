from typing import Optional, List
from pydantic import BaseModel


class RegressionChartData(BaseModel):
    title: str
    bucket_data: List[str]
    reference_data: List[float]
    current_data: Optional[List[float]] = None
