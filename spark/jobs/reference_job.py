import sys
import os
import uuid

import orjson
from pyspark.sql.types import StructField, StructType, StringType

from utils.reference import ReferenceMetricsService
from utils.models import JobStatus, ModelOut
from utils.spark import apply_schema_to_dataframe
from utils.db import update_job_status, write_to_db

from pyspark.sql import SparkSession

import logging


def main(
    spark_session: SparkSession,
    model: ModelOut,
    reference_dataset_path: str,
    reference_uuid: str,
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

    reference_schema = model.to_reference_spark_schema()
    reference_dataset = spark_session.read.csv(reference_dataset_path, header=True)
    reference_dataset = apply_schema_to_dataframe(reference_dataset, reference_schema)
    reference_dataset = reference_dataset.select(
        *[c for c in reference_schema.names if c in reference_dataset.columns]
    )
    metrics_service = ReferenceMetricsService(reference_dataset, model=model)
    model_quality = metrics_service.calculate_model_quality()
    statistics = metrics_service.calculate_statistics()
    data_quality = metrics_service.calculate_data_quality()

    # TODO put needed fields here
    complete_record = {
        "UUID": str(uuid.uuid4()),
        "REFERENCE_UUID": reference_uuid,
        "MODEL_QUALITY": orjson.dumps(model_quality).decode("utf-8"),
        "STATISTICS": orjson.dumps(statistics).decode("utf-8"),
        "DATA_QUALITY": data_quality.model_dump_json(serialize_as_any=True),
    }

    schema = StructType(
        [
            StructField("UUID", StringType(), True),
            StructField("REFERENCE_UUID", StringType(), True),
            StructField("MODEL_QUALITY", StringType(), True),
            StructField("DATA_QUALITY", StringType(), True),
            StructField("STATISTICS", StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, table_name)
    # FIXME table name should come from parameters
    update_job_status(reference_uuid, JobStatus.SUCCEEDED, "reference_dataset")


if __name__ == "__main__":
    spark_session = SparkSession.builder.appName(
        "radicalbit_reference_metrics"
    ).getOrCreate()

    # Json of ModelOut is first param
    model = ModelOut.model_validate_json(sys.argv[1])
    # Reference dataset s3 path is second param
    reference_dataset_path = sys.argv[2]
    # Reference file uuid third param
    reference_uuid = sys.argv[3]
    # Table name fourth param
    table_name = sys.argv[4]

    try:
        main(spark_session, model, reference_dataset_path, reference_uuid, table_name)
    except Exception as e:
        logging.exception(e)
        # FIXME table name should come from parameters
        update_job_status(reference_uuid, JobStatus.ERROR, "reference_dataset")
    finally:
        spark_session.stop()
