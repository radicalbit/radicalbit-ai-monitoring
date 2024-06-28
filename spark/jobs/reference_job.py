import sys
import os
import uuid

import orjson
from pyspark.sql.types import StructField, StructType, StringType

from metrics.statistics import calculate_statistics_reference
from models.reference_dataset import ReferenceDataset
from utils.reference_regression import ReferenceMetricsRegressionService
from utils.reference_binary import ReferenceMetricsService
from utils.models import JobStatus, ModelOut, ModelType
from utils.db import update_job_status, write_to_db

from pyspark.sql import SparkSession

import logging

from utils.reference_multiclass import ReferenceMetricsMulticlassService


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

    raw_dataframe = spark_session.read.csv(reference_dataset_path, header=True)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=raw_dataframe)

    complete_record = {"UUID": str(uuid.uuid4()), "REFERENCE_UUID": reference_uuid}

    match model.model_type:
        case ModelType.BINARY:
            metrics_service = ReferenceMetricsService(
                reference_dataset.reference, model=model
            )
            model_quality = metrics_service.calculate_model_quality()
            statistics = calculate_statistics_reference(reference_dataset)
            data_quality = metrics_service.calculate_data_quality()
            complete_record["MODEL_QUALITY"] = orjson.dumps(model_quality).decode(
                "utf-8"
            )
            complete_record["STATISTICS"] = orjson.dumps(statistics).decode("utf-8")
            complete_record["DATA_QUALITY"] = data_quality.model_dump_json(
                serialize_as_any=True
            )
        case ModelType.MULTI_CLASS:
            metrics_service = ReferenceMetricsMulticlassService(
                reference=reference_dataset
            )
            statistics = calculate_statistics_reference(reference_dataset)
            data_quality = metrics_service.calculate_data_quality()
            model_quality = metrics_service.calculate_model_quality()
            complete_record["STATISTICS"] = orjson.dumps(statistics).decode("utf-8")
            complete_record["DATA_QUALITY"] = data_quality.model_dump_json(
                serialize_as_any=True
            )
            complete_record["MODEL_QUALITY"] = orjson.dumps(model_quality).decode(
                "utf-8"
            )
        case ModelType.REGRESSION:
            metrics_service = ReferenceMetricsRegressionService(
                reference=reference_dataset
            )
            model_quality = metrics_service.calculate_model_quality()
            complete_record["MODEL_QUALITY"] = model_quality.model_dump_json(
                serialize_as_any=True
            )

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
