import logging
import os
import sys
import uuid

from embeddings.embeddings_metrics_calculator import EmbeddingsMetricsCalculator
import orjson
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType, StructField, StructType
from utils.db import update_job_status, write_to_db
from utils.logger import logger_config
from utils.models import JobStatus, ModelOut

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


def compute_metrics(spark_session: SparkSession, reference_dataset: DataFrame):
    complete_record = {}
    embedding = EmbeddingsMetricsCalculator(spark_session, reference_dataset, '', 0.80)
    metrics = embedding.compute_result()
    del metrics['histogram']['distances']
    reference_metrics = {
        'reference_embeddings_metrics': metrics['embeddings_metrics'],
        'histogram': {
            'buckets': metrics['histogram']['buckets'],
            'reference_values': metrics['histogram']['values'],
        },
        'reference_embeddings': metrics['embeddings'],
    }
    complete_record['METRICS'] = orjson.dumps(reference_metrics).decode('utf-8')
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

    raw_dataframe = spark_session.read.csv(
        reference_dataset_path, inferSchema=True, header=True
    )

    complete_record = compute_metrics(spark_session, raw_dataframe)

    complete_record.update(
        {'UUID': str(uuid.uuid4()), 'REFERENCE_UUID': reference_uuid}
    )

    schema = StructType(
        [
            StructField('UUID', StringType(), True),
            StructField('REFERENCE_UUID', StringType(), True),
            StructField('METRICS', StringType(), True),
        ]
    )
    write_to_db(spark_session, complete_record, schema, metrics_table_name)
    update_job_status(reference_uuid, JobStatus.SUCCEEDED, dataset_table_name)


if __name__ == '__main__':
    spark_session = SparkSession.builder.appName(
        'radicalbit_reference_embeddings_metrics'
    ).getOrCreate()

    model = ModelOut.model_validate_json(sys.argv[1])
    embeddings_reference_dataset_path = sys.argv[2]
    embeddings_reference_uuid = sys.argv[3]
    metrics_table_name = sys.argv[4]
    dataset_table_name = sys.argv[5]

    try:
        main(
            spark_session,
            model,
            embeddings_reference_dataset_path,
            embeddings_reference_uuid,
            metrics_table_name,
            dataset_table_name,
        )
    except Exception as e:
        logger.exception(e)
        update_job_status(
            embeddings_reference_uuid, JobStatus.ERROR, dataset_table_name
        )
    finally:
        spark_session.stop()
