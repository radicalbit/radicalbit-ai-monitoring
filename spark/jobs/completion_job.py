import sys
import os
import uuid
import orjson
from pyspark.sql.types import StructField, StructType, StringType

from metrics.completion_metrics import CompletionMetrics
from utils.models import JobStatus
from utils.db import update_job_status, write_to_db, get_model_name

from pyspark.sql import SparkSession, DataFrame

import logging


def compute_metrics(df: DataFrame, model_name: str) -> dict:
    complete_record = {}
    completion_service = CompletionMetrics()
    model_quality = completion_service.extract_metrics(df, model_name)
    complete_record["MODEL_QUALITY"] = orjson.dumps(
        model_quality.model_dump(serialize_as_any=True)
    ).decode("utf-8")
    return complete_record


def main(
    spark_session: SparkSession,
    completion_dataset_path: str,
    completion_uuid: str,
    metrics_table_name: str,
    dataset_table_name: str,
):
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
    df = spark_session.read.option("multiline", "true").json(completion_dataset_path)
    model_name = get_model_name(completion_uuid, dataset_table_name)
    complete_record = compute_metrics(df, model_name)

    complete_record.update(
        {"UUID": str(uuid.uuid4()), "COMPLETION_UUID": completion_uuid}
    )

    schema = StructType(
        [
            StructField("UUID", StringType(), True),
            StructField("COMPLETION_UUID", StringType(), True),
            StructField("MODEL_QUALITY", StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, metrics_table_name)
    update_job_status(completion_uuid, JobStatus.SUCCEEDED, dataset_table_name)


if __name__ == "__main__":
    spark_session = SparkSession.builder.appName(
        "radicalbit_completion_metrics"
    ).getOrCreate()

    completion_dataset_path = sys.argv[1]
    completion_uuid = sys.argv[2]
    metrics_table_name = sys.argv[3]
    dataset_table_name = sys.argv[4]

    try:
        main(
            spark_session,
            completion_dataset_path,
            completion_uuid,
            metrics_table_name,
            dataset_table_name,
        )

    except Exception as e:
        logging.exception(e)
        update_job_status(completion_uuid, JobStatus.ERROR, dataset_table_name)
    finally:
        spark_session.stop()
