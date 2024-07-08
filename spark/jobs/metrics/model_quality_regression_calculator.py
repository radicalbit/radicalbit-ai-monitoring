from pyspark.sql import DataFrame
import pyspark.sql.functions as F

from models.regression_model_quality import RegressionMetricType, ModelQualityRegression
from utils.models import ModelOut
from pyspark.ml.evaluation import RegressionEvaluator
from utils.spark import is_not_null


class ModelQualityRegressionCalculator:
    @staticmethod
    def eval_model_quality_metric(
        model: ModelOut,
        dataframe: DataFrame,
        dataframe_count: int,
        metric_name: RegressionMetricType,
    ) -> float:
        try:
            match metric_name:
                case RegressionMetricType.ADJ_R2:
                    # Source: https://medium.com/analytics-vidhya/adjusted-r-squared-formula-explanation-1ce033e25699
                    # adj_r2 = 1 - (n - 1) / (n - p - 1)
                    # n: number of observations
                    # p: number of indipendent variables (feaures)
                    p: float = len(model.features)
                    n: float = dataframe_count
                    r2: float = (
                        ModelQualityRegressionCalculator.eval_model_quality_metric(
                            model, dataframe, dataframe_count, RegressionMetricType.R2
                        )
                    )
                    return 1 - (1 - r2) * ((n - 1) / (n - p - 1))
                case RegressionMetricType.MAPE:
                    # Source: https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
                    # mape = 100 * (abs(actual - predicted) / actual) / n
                    _dataframe = dataframe.withColumn(
                        "mape",
                        F.abs(
                            (
                                F.col(model.outputs.prediction.name)
                                - F.col(model.target.name)
                            )
                            / F.col(model.target.name)
                        ),
                    )
                    return _dataframe.agg({"mape": "avg"}).collect()[0][0] * 100
                case (
                    RegressionMetricType.MAE
                    | RegressionMetricType.MSE
                    | RegressionMetricType.RMSE
                    | RegressionMetricType.R2
                    | RegressionMetricType.VAR
                ):
                    return RegressionEvaluator(
                        metricName=metric_name.value,
                        labelCol=model.target.name,
                        predictionCol=model.outputs.prediction.name,
                    ).evaluate(dataframe)
        except Exception:
            return float("nan")

    @staticmethod
    def __calc_mq_metrics(
        model: ModelOut, dataframe: DataFrame, dataframe_count: int
    ) -> ModelQualityRegression:
        return ModelQualityRegression(
            **{
                metric_name.value: ModelQualityRegressionCalculator.eval_model_quality_metric(
                    model,
                    dataframe,
                    dataframe_count,
                    metric_name,
                )
                for metric_name in RegressionMetricType
            }
        )

    @staticmethod
    def numerical_metrics(
        model: ModelOut, dataframe: DataFrame, dataframe_count: int
    ) -> ModelQualityRegression:
        # # drop row where prediction or ground_truth is null
        dataframe_clean = dataframe.filter(
            is_not_null(model.outputs.prediction.name) & is_not_null(model.target.name)
        )
        dataframe_clean_count = dataframe_clean.count()
        return ModelQualityRegressionCalculator.__calc_mq_metrics(
            model, dataframe_clean, dataframe_clean_count
        )
