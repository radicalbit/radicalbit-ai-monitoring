import pyspark.sql.functions as F
import numpy as np
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType
from models.completion_dataset import LLMMetricsModel


class LLMMetrics:
    def __init__(self):
        pass

    @staticmethod
    @F.udf(FloatType())
    def compute_probability_udf(log_prob: float) -> float:
        return float(np.exp(log_prob))

    @staticmethod
    @F.udf(FloatType())
    def compute_perplexity(log_probs: list[float]) -> float:
        return float(np.exp(-np.mean(log_probs)))

    @staticmethod
    @F.udf(FloatType())
    def compute_prob_mean_per_phrase(probs: list[float]) -> float:
        return float(np.mean(probs))

    @staticmethod
    def remove_columns(df: DataFrame) -> DataFrame:
        df = df.drop(
            "model",
            "object",
            "created",
            "system_fingerprint",
            "usage",
            "service_tier",
        )
        return df

    def compute_prob(self, df: DataFrame):
        df = df.select(F.explode("choices").alias("element"), F.col("id"))
        df = df.select(
            F.col("id"), F.explode("element.logprobs.content").alias("content")
        )
        df = df.select("id", "content.logprob", "content.token").withColumn(
            "prob", self.compute_probability_udf("logprob")
        )
        return df

    def extract_metrics(self, df: DataFrame) -> LLMMetricsModel:
        df = self.remove_columns(df)
        df = self.compute_prob(df)
        df_prob = df.drop("logprob")
        df_prob = df_prob.groupBy("id").agg(
            F.collect_list(F.struct("token", "prob")).alias("probs")
        )
        df_mean_values = df.groupBy("id").agg(
            self.compute_prob_mean_per_phrase(F.collect_list("prob")).alias(
                "prob_per_phrase"
            ),
            self.compute_perplexity(F.collect_list("logprob")).alias(
                "perplex_per_phrase"
            ),
        )
        df = df_mean_values.agg(
            F.mean("prob_per_phrase").alias("prob_tot_mean"),
            F.mean("perplex_per_phrase").alias("perplex_tot_mean"),
        )
        tokens = [
            {
                "id": row["id"],
                "probs": [
                    {"token": prob["token"], "prob": prob["prob"]}
                    for prob in row["probs"]
                ],
            }
            for row in df_prob.toLocalIterator()
        ]

        res = {
            "tokens": tokens,
            "mean_per_phrase": df_mean_values.toPandas().to_dict(orient="records"),
            "mean_per_file": df.toPandas().to_dict(orient="records"),
        }
        return LLMMetricsModel(**res)
