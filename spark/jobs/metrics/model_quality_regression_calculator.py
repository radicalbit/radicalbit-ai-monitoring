import numpy as np
from math import inf

from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from pyspark.sql.types import ArrayType, FloatType
from pyspark.ml.feature import StandardScaler, VectorAssembler, Bucketizer
from pyspark.ml.stat import KolmogorovSmirnovTest
from pyspark.ml.regression import LinearRegression

from models.regression_model_quality import (
    RegressionMetricType,
    ModelQualityRegression,
    Histogram,
)
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
        prefix_id: str,
    ) -> float:
        try:
            dataframe = dataframe.withColumn(
                model.outputs.prediction.name,
                F.col(model.outputs.prediction.name).cast("float"),
            )
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
                            model,
                            dataframe,
                            dataframe_count,
                            RegressionMetricType.R2,
                            prefix_id,
                        )
                    )
                    return 1 - (1 - r2) * ((n - 1) / (n - p - 1))
                case RegressionMetricType.MAPE:
                    # Source: https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
                    # mape = 100 * (abs(actual - predicted) / actual) / n
                    _dataframe = dataframe.withColumn(
                        f"{prefix_id}_mape",
                        F.abs(
                            (
                                F.col(model.outputs.prediction.name)
                                - F.col(model.target.name)
                            )
                            / F.col(model.target.name)
                        ),
                    )
                    return (
                        _dataframe.agg({f"{prefix_id}_mape": "avg"}).collect()[0][0]
                        * 100
                    )
                case RegressionMetricType.VAR:
                    return RegressionEvaluator(
                        metricName="var",
                        labelCol=model.target.name,
                        predictionCol=model.outputs.prediction.name,
                    ).evaluate(dataframe)
                case (
                    RegressionMetricType.MAE
                    | RegressionMetricType.MSE
                    | RegressionMetricType.RMSE
                    | RegressionMetricType.R2
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
        model: ModelOut, dataframe: DataFrame, dataframe_count: int, prefix_id: str
    ) -> ModelQualityRegression:
        return ModelQualityRegression(
            **{
                metric_name.value: ModelQualityRegressionCalculator.eval_model_quality_metric(
                    model, dataframe, dataframe_count, metric_name, prefix_id
                )
                for metric_name in RegressionMetricType
            }
        )

    @staticmethod
    def numerical_metrics(
        model: ModelOut, dataframe: DataFrame, dataframe_count: int, prefix_id: str
    ) -> ModelQualityRegression:
        # # drop row where prediction or ground_truth is null
        dataframe_clean = dataframe.filter(
            is_not_null(model.outputs.prediction.name) & is_not_null(model.target.name)
        )
        dataframe_clean_count = dataframe_clean.count()
        return ModelQualityRegressionCalculator.__calc_mq_metrics(
            model, dataframe_clean, dataframe_clean_count, prefix_id
        )

    @staticmethod
    def residual_calculation(model: ModelOut, dataframe: DataFrame, prefix_id: str):
        dataframe_clean = dataframe.filter(
            is_not_null(model.outputs.prediction.name) & is_not_null(model.target.name)
        ).select(model.outputs.prediction.name, model.target.name)
        dataframe_clean = dataframe_clean.withColumn(
            f"{prefix_id}_residual",
            F.col(model.target.name) - F.col(model.outputs.prediction.name),
        )
        va = (
            VectorAssembler()
            .setInputCols([f"{prefix_id}_residual"])
            .setOutputCol(f"{prefix_id}_residual_vector")
        )
        data_va = va.transform(dataframe_clean)

        residual_scaler = StandardScaler(
            inputCol=f"{prefix_id}_residual_vector",
            outputCol=f"{prefix_id}_std_residual_vector",
            withMean=True,
            withStd=True,
        )
        residual_scaler_model = residual_scaler.fit(data_va)
        data_scaled = residual_scaler_model.transform(data_va)

        vector2list = F.udf(lambda x: x.toArray().tolist(), ArrayType(FloatType()))
        data_norm = data_scaled.withColumn(
            f"{prefix_id}_std_residual",
            vector2list(F.col(f"{prefix_id}_std_residual_vector")).getItem(0),
        )
        return data_norm

    @staticmethod
    def create_histogram(dataframe: DataFrame, feature: str):
        base_df = dataframe.select(feature)
        max_value = base_df.agg(
            F.max(
                F.when(
                    F.col(feature).isNotNull() & ~F.isnan(feature),
                    F.col(feature),
                )
            )
        ).collect()[0][0]
        min_value = base_df.agg(
            F.min(
                F.when(
                    F.col(feature).isNotNull() & ~F.isnan(feature),
                    F.col(feature),
                )
            )
        ).collect()[0][0]
        buckets_spacing = np.linspace(min_value, max_value, 11).tolist()
        lookup = set()
        generated_buckets = [
            x for x in buckets_spacing if x not in lookup and lookup.add(x) is None
        ]
        # workaround if all values are the same to not have errors
        if len(generated_buckets) == 1:
            buckets_spacing = [generated_buckets[0], generated_buckets[0]]
            buckets = [-float(inf), generated_buckets[0], float(inf)]
        else:
            buckets = generated_buckets

        bucketizer = Bucketizer(splits=buckets, inputCol=feature, outputCol="bucket")
        bucket_result = bucketizer.setHandleInvalid("keep").transform(base_df)
        result_df = (
            bucket_result.groupBy("bucket")
            .agg(F.count(F.col(feature)).alias("value_count"))
            .fillna(0)
            .orderBy("bucket")
        )
        # workaround if all values are the same to not have errors
        if len(generated_buckets) == 1:
            result_df = result_df.filter(F.col("bucket") == 1)
        res = result_df.select("value_count").rdd.flatMap(lambda x: x).collect()
        return Histogram(buckets=buckets_spacing, values=res)

    @staticmethod
    def get_regression_line(model: ModelOut, dataframe: DataFrame, prefix_id: str):
        dataframe_clean = (
            dataframe.filter(
                is_not_null(model.outputs.prediction.name)
                & is_not_null(model.target.name)
            )
            .select(model.outputs.prediction.name, model.target.name)
            .withColumnRenamed(model.outputs.prediction.name, f"{prefix_id}_regr_pred")
        )

        va = VectorAssembler(inputCols=[model.target.name], outputCol="features")

        data_va = va.transform(dataframe_clean)

        train_data = data_va.select("features", f"{prefix_id}_regr_pred")

        lr = LinearRegression(labelCol=f"{prefix_id}_regr_pred")

        # Fit the model to the data and call this model lrModel
        lr_model = lr.fit(train_data)
        c = lr_model.coefficients[0]
        i = lr_model.intercept

        return {"coefficient": float(c), "intercept": float(i)}

    @staticmethod
    def residual_metrics(model: ModelOut, dataframe: DataFrame, prefix_id: str):
        residual_df_norm = ModelQualityRegressionCalculator.residual_calculation(
            model, dataframe, prefix_id
        )
        ks_result = KolmogorovSmirnovTest.test(
            residual_df_norm, f"{prefix_id}_residual", "norm", 0.0, 1.0
        ).first()
        return {
            "ks": {
                "p_value": ks_result.pValue,
                "statistic": ks_result.statistic,
            },
            "correlation_coefficient": dataframe.corr(
                model.outputs.prediction.name, model.target.name
            ),
            "histogram": ModelQualityRegressionCalculator.create_histogram(
                residual_df_norm, f"{prefix_id}_residual"
            ).model_dump(serialize_as_any=True),
            "standardized_residuals": residual_df_norm.select(
                f"{prefix_id}_std_residual"
            )
            .rdd.flatMap(lambda x: x)
            .collect(),
            "predictions": residual_df_norm.select(model.outputs.prediction.name)
            .rdd.flatMap(lambda x: x)
            .collect(),
            "targets": residual_df_norm.select(model.target.name)
            .rdd.flatMap(lambda x: x)
            .collect(),
            "regression_line": ModelQualityRegressionCalculator.get_regression_line(
                model, dataframe, prefix_id
            ),
        }
