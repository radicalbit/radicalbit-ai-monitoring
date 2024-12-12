import logging
import sys
import os
import uuid

import orjson
from pyspark.sql.types import StructType, StructField, StringType

from metrics.percentages import PercentageCalculator
from metrics.statistics import calculate_statistics_current
from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset

from utils.current_binary import CurrentMetricsService
from utils.current_multiclass import CurrentMetricsMulticlassService
from utils.current_regression import CurrentMetricsRegressionService
from utils.models import JobStatus, ModelOut, ModelType
from utils.db import update_job_status, write_to_db

from pyspark.sql import SparkSession


def compute_metrics(spark_session, current_dataset, reference_dataset, model):
    complete_record = {}
    match model.model_type:
        case ModelType.BINARY:
            metrics_service = CurrentMetricsService(
                spark_session=spark_session,
                current=current_dataset,
                reference=reference_dataset,
            )
            statistics = calculate_statistics_current(current_dataset)
            data_quality = metrics_service.calculate_data_quality()
            model_quality = (
                metrics_service.calculate_model_quality_with_group_by_timestamp()
            )
            drift = metrics_service.calculate_drift()
            percentages = PercentageCalculator.calculate_percentages(
                spark_session=spark_session,
                current_dataset=current_dataset,
                reference_dataset=reference_dataset,
                drift=drift,
                model_quality_current=model_quality,
                model=model,
            )
            complete_record["MODEL_QUALITY"] = orjson.dumps(model_quality).decode(
                "utf-8"
            )
            complete_record["STATISTICS"] = statistics.model_dump_json(
                serialize_as_any=True
            )
            complete_record["DATA_QUALITY"] = data_quality.model_dump_json(
                serialize_as_any=True
            )
            complete_record["DRIFT"] = orjson.dumps(drift).decode("utf-8")
            complete_record["PERCENTAGES"] = orjson.dumps(percentages).decode("utf-8")
        case ModelType.MULTI_CLASS:
            metrics_service = CurrentMetricsMulticlassService(
                spark_session=spark_session,
                current=current_dataset,
                reference=reference_dataset,
            )
            statistics = calculate_statistics_current(current_dataset)
            data_quality = metrics_service.calculate_data_quality()
            model_quality = metrics_service.calculate_model_quality()
            drift = metrics_service.calculate_drift()
            percentages = PercentageCalculator.calculate_percentages(
                spark_session=spark_session,
                current_dataset=current_dataset,
                reference_dataset=reference_dataset,
                drift=drift,
                model_quality_current=model_quality,
                model=model,
            )

            complete_record["STATISTICS"] = statistics.model_dump_json(
                serialize_as_any=True
            )
            complete_record["DATA_QUALITY"] = data_quality.model_dump_json(
                serialize_as_any=True
            )
            complete_record["MODEL_QUALITY"] = orjson.dumps(model_quality).decode(
                "utf-8"
            )
            complete_record["DRIFT"] = orjson.dumps(drift).decode("utf-8")
            complete_record["PERCENTAGES"] = orjson.dumps(percentages).decode("utf-8")
        case ModelType.REGRESSION:
            metrics_service = CurrentMetricsRegressionService(
                reference=reference_dataset,
                current=current_dataset,
                spark_session=spark_session,
            )
            statistics = calculate_statistics_current(current_dataset)
            data_quality = metrics_service.calculate_data_quality(is_current=True)
            model_quality = metrics_service.calculate_model_quality()
            drift = metrics_service.calculate_drift()
            percentages = PercentageCalculator.calculate_percentages(
                spark_session=spark_session,
                current_dataset=current_dataset,
                reference_dataset=reference_dataset,
                drift=drift,
                model_quality_current=model_quality,
                model=model,
            )

            complete_record["STATISTICS"] = statistics.model_dump_json(
                serialize_as_any=True
            )
            complete_record["DATA_QUALITY"] = data_quality.model_dump_json(
                serialize_as_any=True
            )
            complete_record["MODEL_QUALITY"] = orjson.dumps(model_quality).decode(
                "utf-8"
            )
            complete_record["DRIFT"] = orjson.dumps(drift).decode("utf-8")
            complete_record["PERCENTAGES"] = orjson.dumps(percentages).decode("utf-8")

    return complete_record


def main(
    spark_session: SparkSession,
    model: ModelOut,
    current_dataset_path: str,
    current_uuid: str,
    reference_dataset_path: str,
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

    raw_current = spark_session.read.csv(current_dataset_path, header=True)
    current_dataset = CurrentDataset(model=model, raw_dataframe=raw_current)
    raw_reference = spark_session.read.csv(reference_dataset_path, header=True)
    reference_dataset = ReferenceDataset(model=model, raw_dataframe=raw_reference)

    complete_record = compute_metrics(
        spark_session=spark_session,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
    )
    complete_record.update({"UUID": str(uuid.uuid4()), "CURRENT_UUID": current_uuid})

    schema = StructType(
        [
            StructField("UUID", StringType(), True),
            StructField("CURRENT_UUID", StringType(), True),
            StructField("STATISTICS", StringType(), True),
            StructField("DATA_QUALITY", StringType(), True),
            StructField("MODEL_QUALITY", StringType(), True),
            StructField("DRIFT", StringType(), True),
            StructField("PERCENTAGES", StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, metrics_table_name)
    update_job_status(current_uuid, JobStatus.SUCCEEDED, dataset_table_name)


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
    # Metrics Table name fifth param
    metrics_table_name = sys.argv[5]
    # Metrics Table name sixth param
    dataset_table_name = sys.argv[6]

    try:
        main(
            spark_session,
            model,
            current_dataset_path,
            current_uuid,
            reference_dataset_path,
            metrics_table_name,
        )
    except Exception as e:
        logging.exception(e)
        update_job_status(current_uuid, JobStatus.ERROR, dataset_table_name)
    finally:
        spark_session.stop()
