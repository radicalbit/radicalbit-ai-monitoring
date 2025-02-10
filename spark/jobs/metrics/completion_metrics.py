import pyspark.sql.functions as F
import numpy as np
from pyspark.sql import DataFrame
from pyspark.sql.types import FloatType
from models.completion_dataset import CompletionMetricsModel
from datetime import datetime


class CompletionMetrics:
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
            "object",
            "system_fingerprint",
            "service_tier",
        )
        return df

    def compute_prob(self, df: DataFrame):
        df = df.select(
            F.explode("choices").alias("element"),
            F.col("usage.completion_tokens").alias("tot_tokens"),
            F.col("id"),
            F.col("model"),
            F.col("created"),
        )
        df = df.select(
            F.col("id"),
            F.col("model"),
            F.col("created"),
            F.col("tot_tokens"),
            F.col("element.message.content").alias("message_content"),
            F.explode("element.logprobs.content").alias("content"),
        )
        df = df.select(
            "id",
            "message_content",
            "content.logprob",
            "content.token",
            "model",
            "created",
            "tot_tokens",
        ).withColumn("prob", self.compute_probability_udf("logprob"))
        return df

    def extract_metrics(self, df: DataFrame) -> CompletionMetricsModel:
        df = self.remove_columns(df)
        df = self.compute_prob(df)
        df_prob = df.drop("logprob")
        df_prob = df_prob.groupBy(
            "id", "message_content", "model", "created", "tot_tokens"
        ).agg(F.collect_list(F.struct("token", "prob")).alias("probs"))
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
        df_prob = df_prob.orderBy("id")
        tokens = [
            {
                "id": row["id"],
                "message_content": row["message_content"],
                "probs": [
                    {"token": prob["token"], "prob": prob["prob"]}
                    for prob in row["probs"]
                ],
                "timestamp": datetime.fromtimestamp(row["created"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "model_name": row["model"],
                "total_token": row["tot_tokens"],
                "prob": df_mean_values.filter(F.col("id") == row["id"])
                .select("prob_per_phrase")
                .first()[0],
                "perplex": df_mean_values.filter(F.col("id") == row["id"])
                .select("perplex_per_phrase")
                .first()[0],
            }
            for row in df_prob.toLocalIterator()
        ]
        res = {
            "tokens": tokens,
            "mean_per_file": df.toPandas().to_dict(orient="records"),
        }
        return CompletionMetricsModel(**res)
