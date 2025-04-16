import logging
import os
import sys
import uuid

from models.current_dataset import CurrentDataset
from models.reference_dataset import ReferenceDataset
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructField, StructType
from utils.db import update_job_status, write_to_db
from utils.logger import logger_config
from utils.models import JobStatus, ModelOut

logger = logging.getLogger(logger_config.get('logger_name', 'default'))


def compute_metrics(
    spark_session, current_dataset, reference_dataset, model, current_id
):
    # TODO: Define the logic of computing embeddings metrics
    return {}


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

    raw_current = spark_session.read.csv(current_dataset_path, header=True)
    current_dataset = CurrentDataset(
        model=model, raw_dataframe=raw_current, prefix_id=current_uuid
    )
    raw_reference = spark_session.read.csv(reference_dataset_path, header=True)
    reference_dataset = ReferenceDataset(
        model=model, raw_dataframe=raw_reference, prefix_id=current_uuid
    )

    complete_record = compute_metrics(
        spark_session=spark_session,
        current_dataset=current_dataset,
        reference_dataset=reference_dataset,
        model=model,
        current_id=current_uuid,
    )
    complete_record.update({'UUID': str(uuid.uuid4()), 'CURRENT_UUID': current_uuid})

    schema = StructType(
        [
            StructField('UUID', StringType(), True),
            StructField('CURRENT_UUID', StringType(), True),
            StructField('METRICS', StringType(), True),
            StructField('DRIFT', StringType(), True),
        ]
    )

    write_to_db(spark_session, complete_record, schema, metrics_table_name)
    update_job_status(current_uuid, JobStatus.SUCCEEDED, dataset_table_name)


if __name__ == '__main__':
    spark_session = SparkSession.builder.appName(
        'radicalbit_current_embeddings_metrics'
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
            dataset_table_name,
        )
    except Exception as e:
        logger.exception(e)
        update_job_status(current_uuid, JobStatus.ERROR, dataset_table_name)
    finally:
        spark_session.stop()
