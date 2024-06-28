from pydantic import BaseModel

from enum import Enum


class RegressionMetricType(str, Enum):
    MAE = "mae"
    MAPE = "mape"
    MSE = "mse"
    RMSE = "rmse"
    R2 = "r2"
    ADJ_R2 = "adj_r2"
    VAR = "var"


class ModelQualityRegression(BaseModel):
    mae: float
    mape: float
    mse: float
    rmse: float
    r2: float
    adj_r2: float
    var: float
