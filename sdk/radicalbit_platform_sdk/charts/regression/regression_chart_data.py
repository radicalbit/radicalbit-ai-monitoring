from typing import List, Optional

from pydantic import BaseModel


class RegressionDistributionChartData(BaseModel):
    title: str
    bucket_data: List[str]
    reference_data: List[float]
    current_data: Optional[List[float]] = None

class RegressionPredictedActualChartData(BaseModel):
    scatter_data: List[List[float]]
    coefficient: float
    intercept: float
    color: Optional[str] = '#9B99A1'

class RegressionResidualScatterChartData(BaseModel):
    scatter_data: List[List[float]]
    color: Optional[str] = '#9B99A1'

class RegressionResidualBucketChartData(BaseModel):
    bucket_data: List[str]
    values: List[float]
    color: Optional[str] = '#3695d9'
