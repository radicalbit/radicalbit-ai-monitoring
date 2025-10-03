import logging
import os
import sys
import uuid

from embeddings.embeddings_metrics_calculator import EmbeddingsMetricsCalculator
from metrics.drift_calculator import DriftCalculator
import orjson
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import DoubleType, StringType, StructField, StructType
from utils.db import update_job_status, write_to_db
from utils.logger import logger_config
from utils.models import JobStatus, ModelOut

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


def compute_metrics(
    spark_session: SparkSession,
    current_dataset: DataFrame,
    reference_dataset: DataFrame,
) -> dict:
    complete_record = {}
    cur_embedding_calculator = EmbeddingsMetricsCalculator(
        spark_session, current_dataset, 'rb', 0.80
    )
    cur_emdeddings = cur_embedding_calculator.compute_result()
    ref_embedding_calculator = EmbeddingsMetricsCalculator(
        spark_session, reference_dataset, 'rb', 0.80
    )
    ref_emdeddings = ref_embedding_calculator.compute_result()
    schema = StructType(
        [StructField(name='distance', dataType=DoubleType(), nullable=True)]
    )
    drift_score = DriftCalculator.calculate_embeddings_drift(
        spark_session,
        spark_session.createDataFrame(
            data=[(f,) for f in ref_emdeddings['histogram']['distances']], schema=schema
        ),
        spark_session.createDataFrame(
            data=[(f,) for f in cur_emdeddings['histogram']['distances']], schema=schema
        ),
        'rb',
    )
    metrics = {
        'reference_embeddings_metrics': ref_emdeddings['embeddings_metrics'],
        'reference_embeddings': ref_emdeddings['embeddings'],
        'current_embeddings_metrics': cur_emdeddings['embeddings_metrics'],
        'current_embeddings': cur_emdeddings['embeddings'],
        'histogram': {
            'buckets': ref_emdeddings['histogram']['buckets'],
            'reference_values': ref_emdeddings['histogram']['values'],
            'current_values': cur_emdeddings['histogram']['values'],
            'distances_ref': ref_emdeddings['histogram']['distances'],
            'distances_cur': cur_emdeddings['histogram']['distances'],
        },
    }
    complete_record['METRICS'] = orjson.dumps(metrics).decode('utf-8')
    complete_record['DRIFT_SCORE'] = orjson.dumps(drift_score).decode('utf-8')
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

    raw_current = spark_session.read.csv(
        current_dataset_path, header=True, inferSchema=True
    )
    raw_reference = spark_session.read.csv(
        reference_dataset_path, header=True, inferSchema=True
    )

    complete_record = compute_metrics(
        spark_session=spark_session,
        current_dataset=raw_current,
        reference_dataset=raw_reference,
    )
    complete_record.update({'UUID': str(uuid.uuid4()), 'CURRENT_UUID': current_uuid})
    schema = StructType(
        [
            StructField('UUID', StringType(), True),
            StructField('CURRENT_UUID', StringType(), True),
            StructField('METRICS', StringType(), True),
            StructField('DRIFT_SCORE', StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, metrics_table_name)
    update_job_status(current_uuid, JobStatus.SUCCEEDED, dataset_table_name)


if __name__ == '__main__':
    spark_session = SparkSession.builder.appName('radicalbit_completion_metrics')

    if os.getenv('S3_ENDPOINT_URL'):
        endpoint = os.getenv('S3_ENDPOINT_URL')
        if endpoint.startswith('https://'):
            # We are using deployed MinIO over https
            spark_session.config(
                'spark.driver.extraJavaOptions',
                '-Dcom.amazonaws.sdk.disableCertChecking',
            ).config(
                'spark.executor.extraJavaOptions',
                '-Dcom.amazonaws.sdk.disableCertChecking',
            )

    spark_session = spark_session.getOrCreate()

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
            dataset_table_name,
        )
    except Exception as e:
        logger.exception(e)
        update_job_status(current_uuid, JobStatus.ERROR, dataset_table_name)
    finally:
        spark_session.stop()
