import logging
import os
import sys
import uuid

from metrics.statistics import calculate_statistics_reference
from models.reference_dataset import ReferenceDataset
import orjson
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType
from utils.db import update_job_status, write_to_db
from utils.logger import logger_config
from utils.models import JobStatus, ModelOut, ModelType
from utils.reference_binary import ReferenceMetricsService
from utils.reference_multiclass import ReferenceMetricsMulticlassService
from utils.reference_regression import ReferenceMetricsRegressionService

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


def compute_metrics(reference_dataset, model, reference_uuid):
    complete_record = {}
    match model.model_type:
        case ModelType.BINARY:
            metrics_service = ReferenceMetricsService(
                reference=reference_dataset, prefix_id=reference_uuid
            )
            model_quality = metrics_service.calculate_model_quality()
            statistics = calculate_statistics_reference(reference_dataset)
            data_quality = metrics_service.calculate_data_quality()
            complete_record['MODEL_QUALITY'] = orjson.dumps(model_quality).decode(
                'utf-8'
            )
            complete_record['STATISTICS'] = statistics.model_dump_json(
                serialize_as_any=True
            )
            complete_record['DATA_QUALITY'] = data_quality.model_dump_json(
                serialize_as_any=True
            )
        case ModelType.MULTI_CLASS:
            metrics_service = ReferenceMetricsMulticlassService(
                reference=reference_dataset, prefix_id=reference_uuid
            )
            statistics = calculate_statistics_reference(reference_dataset)
            data_quality = metrics_service.calculate_data_quality()
            model_quality = metrics_service.calculate_model_quality()
            complete_record['STATISTICS'] = statistics.model_dump_json(
                serialize_as_any=True
            )
            complete_record['DATA_QUALITY'] = data_quality.model_dump_json(
                serialize_as_any=True
            )
            complete_record['MODEL_QUALITY'] = orjson.dumps(model_quality).decode(
                'utf-8'
            )
        case ModelType.REGRESSION:
            metrics_service = ReferenceMetricsRegressionService(
                reference=reference_dataset, prefix_id=reference_uuid
            )
            statistics = calculate_statistics_reference(reference_dataset)
            data_quality = metrics_service.calculate_data_quality()
            model_quality = metrics_service.calculate_model_quality()

            complete_record['STATISTICS'] = statistics.model_dump_json(
                serialize_as_any=True
            )
            complete_record['MODEL_QUALITY'] = orjson.dumps(model_quality).decode(
                'utf-8'
            )
            complete_record['DATA_QUALITY'] = data_quality.model_dump_json(
                serialize_as_any=True
            )
    return complete_record


def main(
    spark_session: SparkSession,
    model: ModelOut,
    reference_dataset_path: str,
    reference_uuid: str,
    metrics_table_name: str,
    dataset_table_name: str,
):
    spark_context = spark_session.sparkContext

    spark_context._jsc.hadoopConfiguration().set(
        'fs.s3a.access.key', os.getenv('AWS_ACCESS_KEY_ID')
    )
    spark_context._jsc.hadoopConfiguration().set(
        'fs.s3a.secret.key', os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    spark_context._jsc.hadoopConfiguration().set(
        'fs.s3a.endpoint.region', os.getenv('AWS_REGION')
    )
    if os.getenv('S3_ENDPOINT_URL'):
        spark_context._jsc.hadoopConfiguration().set(
            'fs.s3a.endpoint', os.getenv('S3_ENDPOINT_URL')
        )
        spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.style.access', 'true')
        spark_context._jsc.hadoopConfiguration().set(
            'fs.s3a.connection.ssl.enabled', 'false'
        )

    raw_dataframe = spark_session.read.csv(reference_dataset_path, header=True)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_dataframe, prefix_id=reference_uuid
    )

    complete_record = compute_metrics(reference_dataset, model, reference_uuid)

    complete_record.update(
        {'UUID': str(uuid.uuid4()), 'REFERENCE_UUID': reference_uuid}
    )

    schema = StructType(
        [
            StructField('UUID', StringType(), True),
            StructField('REFERENCE_UUID', StringType(), True),
            StructField('MODEL_QUALITY', StringType(), True),
            StructField('DATA_QUALITY', StringType(), True),
            StructField('STATISTICS', StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, metrics_table_name)
    update_job_status(reference_uuid, JobStatus.SUCCEEDED, dataset_table_name)


if __name__ == '__main__':
    spark_session = SparkSession.builder.appName(
        'radicalbit_reference_metrics'
    ).getOrCreate()

    # Json of ModelOut is first param
    model = ModelOut.model_validate_json(sys.argv[1])
    # Reference dataset s3 path is second param
    reference_dataset_path = sys.argv[2]
    # Reference file uuid third param
    reference_uuid = sys.argv[3]
    # Metrics table name fourth param
    metrics_table_name = sys.argv[4]
    # Dataset table name fourth param
    dataset_table_name = sys.argv[5]

    try:
        main(
            spark_session,
            model,
            reference_dataset_path,
            reference_uuid,
            metrics_table_name,
            dataset_table_name,
        )
    except Exception as e:
        logger.exception(e)
        update_job_status(reference_uuid, JobStatus.ERROR, dataset_table_name)
    finally:
        spark_session.stop()
