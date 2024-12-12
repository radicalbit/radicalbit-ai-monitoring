import sys
import os
import uuid

import orjson
from pyspark.sql.types import StructField, StructType, StringType

from metrics.llm_metrics import LLMMetrics
from utils.models import JobStatus
from utils.db import update_job_status, write_to_db

from pyspark.sql import SparkSession, DataFrame

import logging


def compute_metrics(df: DataFrame) -> dict:
    complete_record = {}
    metrics_service = LLMMetrics()
    model_quality = metrics_service.extract_metrics(df)
    complete_record["MODEL_QUALITY"] = orjson.dumps(model_quality.model_dump()).decode(
        "utf-8"
    )
    return complete_record


def main(spark_session: SparkSession, input_path: str, llm_uuid: str, table_name: str):
    spark_context = spark_session.sparkContext

    spark_context._jsc.hadoopConfiguration().set(
        "fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")
    )
    spark_context._jsc.hadoopConfiguration().set(
        "fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    spark_context._jsc.hadoopConfiguration().set(
        "fs.s3a.endpoint.region", os.getenv("AWS_REGION")
    )
    if os.getenv("S3_ENDPOINT_URL"):
        spark_context._jsc.hadoopConfiguration().set(
            "fs.s3a.endpoint", os.getenv("S3_ENDPOINT_URL")
        )
        spark_context._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
        spark_context._jsc.hadoopConfiguration().set(
            "fs.s3a.connection.ssl.enabled", "false"
        )
    df = spark_session.read.option("multiline", "true").json(input_path)
    complete_record = compute_metrics(df)

    complete_record.update({"UUID": str(uuid.uuid4()), "LLM_UUID": llm_uuid})

    schema = StructType(
        [
            StructField("UUID", StringType(), True),
            StructField("LLM_UUID", StringType(), True),
            StructField("MODEL_QUALITY", StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, table_name)
    # # FIXME table name should come from parameters
    update_job_status(llm_uuid, JobStatus.SUCCEEDED, "llm_dataset")


if __name__ == "__main__":
    spark_session = SparkSession.builder.appName(
        "radicalbit_reference_metrics"
    ).getOrCreate()

    # Reference dataset s3 path is second param
    input_path = sys.argv[1]
    # Reference file uuid third param
    llm_uuid = sys.argv[2]
    # Table name fourth param
    table_name = sys.argv[3]

    try:
        main(spark_session, input_path, llm_uuid, table_name)

    except Exception as e:
        logging.exception(e)
        # FIXME table name should come from parameters
        update_job_status(llm_uuid, JobStatus.ERROR, "llm_dataset")
    finally:
        spark_session.stop()
