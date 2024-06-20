import logging
import sys
import os
import uuid

import orjson
from pyspark.sql.types import StructType, StructField, StringType

from utils.current import CurrentMetricsService
from utils.models import JobStatus, ModelOut
from utils.spark import apply_schema_to_dataframe
from utils.db import update_job_status, write_to_db

from pyspark.sql import SparkSession


def main(
    spark_session: SparkSession,
    model: ModelOut,
    current_dataset_path: str,
    current_uuid: str,
    reference_dataset_path: str,
    table_name: str,
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

    current_schema = model.to_current_spark_schema()
    current_dataset = spark_session.read.csv(current_dataset_path, header=True)
    current_dataset = apply_schema_to_dataframe(current_dataset, current_schema)
    current_dataset = current_dataset.select(
        *[c for c in current_schema.names if c in current_dataset.columns]
    )
    reference_schema = model.to_reference_spark_schema()
    reference_dataset = spark_session.read.csv(reference_dataset_path, header=True)
    reference_dataset = apply_schema_to_dataframe(reference_dataset, reference_schema)
    reference_dataset = reference_dataset.select(
        *[c for c in reference_schema.names if c in reference_dataset.columns]
    )
    metrics_service = CurrentMetricsService(
        spark_session, current_dataset, reference_dataset, model=model
    )
    statistics = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()
    model_quality = metrics_service.calculate_model_quality_with_group_by_timestamp()
    drift = metrics_service.calculate_drift()

    # TODO put needed fields here
    complete_record = {
        "UUID": str(uuid.uuid4()),
        "CURRENT_UUID": current_uuid,
        "STATISTICS": orjson.dumps(statistics).decode("utf-8"),
        "DATA_QUALITY": data_quality.model_dump_json(serialize_as_any=True),
        "MODEL_QUALITY": orjson.dumps(model_quality).decode("utf-8"),
        "DRIFT": orjson.dumps(drift).decode("utf-8"),
    }

    schema = StructType(
        [
            StructField("UUID", StringType(), True),
            StructField("CURRENT_UUID", StringType(), True),
            StructField("STATISTICS", StringType(), True),
            StructField("DATA_QUALITY", StringType(), True),
            StructField("MODEL_QUALITY", StringType(), True),
            StructField("DRIFT", StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, table_name)
    # FIXME table name should come from parameters
    update_job_status(current_uuid, JobStatus.SUCCEEDED, "current_dataset")


if __name__ == "__main__":
    spark_session = SparkSession.builder.appName(
        "radicalbit_reference_metrics"
    ).getOrCreate()

    # Json of ModelOut is first param
    model = ModelOut.model_validate_json(sys.argv[1])
    # Current dataset s3 path is second param
    current_dataset_path = sys.argv[2]
    # Current file uuid third param
    current_uuid = sys.argv[3]
    # Reference dataset s3 path is fourth param
    reference_dataset_path = sys.argv[4]
    # Table name fifth param
    table_name = sys.argv[5]

    try:
        main(
            spark_session,
            model,
            current_dataset_path,
            current_uuid,
            reference_dataset_path,
            table_name,
        )
    except Exception as e:
        logging.exception(e)
        # FIXME table name should come from parameters
        update_job_status(current_uuid, JobStatus.ERROR, "current_dataset")
    finally:
        spark_session.stop()
