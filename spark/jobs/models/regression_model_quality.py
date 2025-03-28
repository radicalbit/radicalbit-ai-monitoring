from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class RegressionMetricType(str, Enum):
    MAE = 'mae'
    MAPE = 'mape'
    MSE = 'mse'
    RMSE = 'rmse'
    R2 = 'r2'
    ADJ_R2 = 'adj_r2'
    VAR = 'variance'


class ModelQualityRegression(BaseModel):
    mae: float
    mape: float
    mse: float
    rmse: float
    r2: float
    adj_r2: float
    variance: float


class Histogram(BaseModel):
    buckets: List[float]
    values: Optional[List[int]] = None

    model_config = ConfigDict(ser_json_inf_nan='null')
