from functools import lru_cache
import logging
from typing import Dict, List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

base_dir = 'resources'


class ClickHouseConfig(BaseSettings):
    db_host: str = 'localhost'
    db_port: int = 9002
    db_user: str = 'default'
    db_pwd: str = 'default'
    db_name: str = 'default'
    db_schema: str = 'default'


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{base_dir}/db.conf')

    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'postgres'
    db_pwd: str = 'postgres'
    db_name: str = 'postgres'
    db_schema: str = 'public'


class FileUploadConfig(BaseSettings):
    """File upload configuration to be set for the server"""

    model_config = SettingsConfigDict(env_file=f'{base_dir}/files.conf')

    max_mega_bytes: int = 50
    accepted_file_types: List[str] = ['.csv']

    @property
    def max_bytes(self):
        return self.max_mega_bytes * 1024 * 1024


class KubernetesConfig(BaseSettings):
    """Config to interact with Kubernetes Cluster"""

    model_config = SettingsConfigDict(env_file=f'{base_dir}/kubernetes.conf')

    kubeconfig_file_path: Optional[str] = None


class S3Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{base_dir}/s3.conf')

    aws_access_key_id: str = 'access-key'
    aws_secret_access_key: str = 'secret-key'
    aws_region: str = 'us-east-1'
    s3_endpoint_url: Optional[str] = None
    s3_bucket_name: str = 'test-bucket'


class SparkConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{base_dir}/spark.conf')

    spark_image: str = 'radicalbit/radicalbit-spark-py:latest'
    spark_image_pull_policy: str = 'IfNotPresent'
    spark_reference_app_path: str = 'local:///opt/spark/custom_jobs/reference_job.py'
    spark_current_app_path: str = 'local:///opt/spark/custom_jobs/current_job.py'
    spark_completion_app_path: str = 'local:///opt/spark/custom_jobs/completion_job.py'
    spark_namespace: str = 'spark'
    spark_service_account: str = 'spark'


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return record.getMessage().find('/healthcheck') == -1


class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    model_config = SettingsConfigDict(env_file=f'{base_dir}/logger.conf')
    logger_name: str = 'radicalbit-ai-monitoring'
    log_format: str = '%(levelname)s | %(asctime)s | %(message)s'
    log_level: str = 'DEBUG'

    # logger dictConfig
    version: int = 1
    disable_existing_loggers: bool = False

    formatters: Dict = {
        'default': {
            'format': log_format,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'access': {
            'format': log_format,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }

    filters: Dict = {
        'healthcheck_filter': {'()': HealthCheckFilter},
    }
    handlers: Dict = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['healthcheck_filter'],
        },
    }
    loggers: Dict = {
        logger_name: {
            'handlers': ['default'],
            'level': log_level.upper(),
            'propagate': False,
        },
        'uvicorn.error': {
            'handlers': ['default'],
            'level': log_level.upper(),
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': log_level.upper(),
            'propagate': False,
        },
        'root': {
            'handlers': ['default'],
            'level': log_level.upper(),
            'propagate': False,
        },
    }


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{base_dir}/application.conf')
    http_interface: str = '0.0.0.0'
    http_port: int = 9000
    log_config: LogConfig = LogConfig()
    db_config: DBConfig = DBConfig()
    file_upload_config: FileUploadConfig = FileUploadConfig()
    kubernetes_config: KubernetesConfig = KubernetesConfig()
    s3_config: S3Config = S3Config()
    spark_config: SparkConfig = SparkConfig()
    clickhouse_config: ClickHouseConfig = ClickHouseConfig()


@lru_cache
def get_config():
    return AppConfig()


def create_secrets():
    config = get_config()
    s3_config = config.s3_config
    db_config = config.db_config

    return {
        'AWS_ACCESS_KEY_ID': s3_config.aws_access_key_id,
        'AWS_SECRET_ACCESS_KEY': s3_config.aws_secret_access_key,
        'AWS_REGION': s3_config.aws_region,
        'S3_ENDPOINT_URL': s3_config.s3_endpoint_url,
        'POSTGRES_URL': f'jdbc:postgresql://{db_config.db_host}:{db_config.db_port}/{db_config.db_name}',
        'POSTGRES_DB': db_config.db_name,
        'POSTGRES_HOST': db_config.db_host,
        'POSTGRES_PORT': f'{db_config.db_port}',
        'POSTGRES_USER': db_config.db_user,
        'POSTGRES_PASSWORD': db_config.db_pwd,
        'POSTGRES_SCHEMA': db_config.db_schema,
    }
