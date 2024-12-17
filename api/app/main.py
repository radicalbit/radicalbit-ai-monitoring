from contextlib import asynccontextmanager
import logging
from logging.config import dictConfig

import boto3
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from spark_on_k8s.client import SparkOnK8S
from spark_on_k8s.k8s.sync_client import KubernetesClientManager
from starlette.middleware.cors import CORSMiddleware

from app.core import get_config
from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.completion_dataset_metrics_dao import CompletionDatasetMetricsDAO
from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.model_dao import ModelDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_metrics_dao import ReferenceDatasetMetricsDAO
from app.db.database import Database
from app.models.exceptions import (
    MetricsError,
    ModelError,
    SchemaException,
    internal_exception_handler,
    metrics_exception_handler,
    model_exception_handler,
    request_validation_exception_handler,
    schema_exception_handler,
)
from app.routes.healthcheck_route import HealthcheckRoute
from app.routes.infer_schema_route import InferSchemaRoute
from app.routes.metrics_route import MetricsRoute
from app.routes.model_route import ModelRoute
from app.routes.upload_dataset_route import UploadDatasetRoute
from app.services.file_service import FileService
from app.services.metrics_service import MetricsService
from app.services.model_service import ModelService
from app.services.spark_k8s_service import SparkK8SService

dictConfig(get_config().log_config.model_dump())
logger = logging.getLogger(get_config().log_config.logger_name)

database = Database(get_config().db_config)

if get_config().kubernetes_config.kubeconfig_file_path:
    k8s_client_manager = KubernetesClientManager(
        get_config().kubernetes_config.kubeconfig_file_path
    )
else:
    k8s_client_manager = KubernetesClientManager()

spark_k8s_client = SparkOnK8S(k8s_client_manager=k8s_client_manager)

model_dao = ModelDAO(database)
reference_dataset_dao = ReferenceDatasetDAO(database)
reference_dataset_metrics_dao = ReferenceDatasetMetricsDAO(database)
current_dataset_dao = CurrentDatasetDAO(database)
current_dataset_metrics_dao = CurrentDatasetMetricsDAO(database)
completion_dataset_dao = CompletionDatasetDAO(database)
completion_dataset_metrics_dao = CompletionDatasetMetricsDAO(database)

model_service = ModelService(
    model_dao=model_dao,
    reference_dataset_dao=reference_dataset_dao,
    current_dataset_dao=current_dataset_dao,
    completion_dataset_dao=completion_dataset_dao,
)
s3_config = get_config().s3_config

if s3_config.s3_endpoint_url is not None:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=s3_config.aws_access_key_id,
        aws_secret_access_key=s3_config.aws_secret_access_key,
        region_name=s3_config.aws_region,
        endpoint_url=s3_config.s3_endpoint_url,
    )
else:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=s3_config.aws_access_key_id,
        aws_secret_access_key=s3_config.aws_secret_access_key,
        region_name=s3_config.aws_region,
    )

file_service = FileService(
    reference_dataset_dao,
    current_dataset_dao,
    completion_dataset_dao,
    model_service,
    s3_client,
    spark_k8s_client,
)
metrics_service = MetricsService(
    reference_dataset_metrics_dao=reference_dataset_metrics_dao,
    reference_dataset_dao=reference_dataset_dao,
    current_dataset_metrics_dao=current_dataset_metrics_dao,
    current_dataset_dao=current_dataset_dao,
    completion_dataset_metrics_dao=completion_dataset_metrics_dao,
    completion_dataset_dao=completion_dataset_dao,
    model_service=model_service,
)
spark_k8s_service = SparkK8SService(spark_k8s_client)


@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    logger.info('Starting service ...')
    database.connect()
    database.init_mappings()
    yield
    logger.info('Stopping service ...')


app = FastAPI(title='Radicalbit Platform', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=[
        'access-control-allow-origin',
        'content-type',
    ],
)

app.include_router(ModelRoute.get_router(model_service), prefix='/api/models')
app.include_router(UploadDatasetRoute.get_router(file_service), prefix='/api/models')
app.include_router(InferSchemaRoute.get_router(file_service), prefix='/api/schema')
app.include_router(MetricsRoute.get_router(metrics_service), prefix='/api/models')

app.include_router(HealthcheckRoute.get_healthcheck_route())

app.add_exception_handler(ModelError, model_exception_handler)
app.add_exception_handler(MetricsError, metrics_exception_handler)
app.add_exception_handler(SchemaException, schema_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)
