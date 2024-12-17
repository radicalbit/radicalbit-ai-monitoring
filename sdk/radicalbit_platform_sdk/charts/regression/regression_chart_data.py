from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class RegressionDistributionChartData(BaseModel):
    title: str
    bucket_data: List[float]
    reference_data: List[float]
    current_data: Optional[List[float]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class RegressionPredictedActualChartData(BaseModel):
    scatter_data: List[List[float]]
    coefficient: float
    intercept: float
    color: str = '#9B99A1'


class RegressionResidualScatterChartData(BaseModel):
    scatter_data: List[List[float]]
    color: str = '#9B99A1'


class RegressionResidualBucketChartData(BaseModel):
    bucket_data: List[float]
    values: List[float]
    color: str = '#9B99A1'
