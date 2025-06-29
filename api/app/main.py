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
from app.db.clickhouse_database import ClickHouseDatabase
from app.db.dao.api_key_dao import ApiKeyDAO
from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.completion_dataset_metrics_dao import CompletionDatasetMetricsDAO
from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.current_dataset_embeddings_metrics_dao import (
    CurrentDatasetEmbeddingsMetricsDAO,
)
from app.db.dao.current_dataset_metrics_dao import CurrentDatasetMetricsDAO
from app.db.dao.model_dao import ModelDAO
from app.db.dao.project_dao import ProjectDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.dao.reference_dataset_embeddings_metrics_dao import (
    ReferenceDatasetEmbeddingsMetricsDAO,
)
from app.db.dao.reference_dataset_metrics_dao import ReferenceDatasetMetricsDAO
from app.db.dao.traces_dao import TraceDAO
from app.db.database import Database
from app.models.exceptions import (
    ApiKeyError,
    GenericValidationError,
    MetricsError,
    ModelError,
    OtelError,
    ProjectError,
    SchemaException,
    TraceError,
    api_key_exception_handler,
    generic_validation_exception_handler,
    internal_exception_handler,
    metrics_exception_handler,
    model_exception_handler,
    otel_exception_handler,
    project_exception_handler,
    request_validation_exception_handler,
    schema_exception_handler,
    trace_exception_handler,
)
from app.routes.api_key_route import ApiKeyRoute
from app.routes.healthcheck_route import HealthcheckRoute
from app.routes.infer_schema_route import InferSchemaRoute
from app.routes.metrics_route import MetricsRoute
from app.routes.model_route import ModelRoute
from app.routes.otel_route import OtelRoute
from app.routes.project_route import ProjectRoute
from app.routes.trace_route import TraceRoute
from app.routes.upload_dataset_route import UploadDatasetRoute
from app.services.api_key_security import ApiKeySecurity
from app.services.api_key_service import ApiKeyService
from app.services.file_service import FileService
from app.services.metrics_service import MetricsService
from app.services.model_service import ModelService
from app.services.otel_service import OtelService
from app.services.project_service import ProjectService
from app.services.spark_k8s_service import SparkK8SService
from app.services.trace_service import TraceService

dictConfig(get_config().log_config.model_dump())
logger = logging.getLogger(get_config().log_config.logger_name)

database = Database(conf=get_config().db_config)
ch_database = ClickHouseDatabase(conf=get_config().clickhouse_config)

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
reference_dataset_embeddings_metrics_dao = ReferenceDatasetEmbeddingsMetricsDAO(
    database
)
current_dataset_embeddings_metrics_dao = CurrentDatasetEmbeddingsMetricsDAO(database)
project_dao = ProjectDAO(database)
trace_dao = TraceDAO(ch_database)
api_key_dao = ApiKeyDAO(database)

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
    reference_dataset_embeddings_metrics_dao=reference_dataset_embeddings_metrics_dao,
    current_dataset_embeddings_metrics_dao=current_dataset_embeddings_metrics_dao,
    model_service=model_service,
)
api_key_security = ApiKeySecurity()
api_key_service = ApiKeyService(
    api_key_dao=api_key_dao, project_dao=project_dao, api_key_security=api_key_security
)
project_service = ProjectService(
    project_dao=project_dao, trace_dao=trace_dao, api_key_security=api_key_security
)
trace_service = TraceService(trace_dao=trace_dao, project_dao=project_dao)
otel_service = OtelService(api_key_dao=api_key_dao)
spark_k8s_service = SparkK8SService(spark_k8s_client)


@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    logger.info('Starting service ...')
    database.connect()
    ch_database.connect()
    database.init_mappings()
    yield
    logger.info('Stopping service ...')


app = FastAPI(title='Radicalbit Platform', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=[
        'access-control-allow-origin',
        'content-type',
    ],
)

app.include_router(ModelRoute.get_router(model_service), prefix='/api/models')
app.include_router(UploadDatasetRoute.get_router(file_service), prefix='/api/models')
app.include_router(InferSchemaRoute.get_router(file_service), prefix='/api/schema')
app.include_router(MetricsRoute.get_router(metrics_service), prefix='/api/models')
app.include_router(ProjectRoute.get_router(project_service), prefix='/api/projects')
app.include_router(TraceRoute.get_router(trace_service), prefix='/api/traces')
app.include_router(ApiKeyRoute.get_router(api_key_service), prefix='/api/api-key')
app.include_router(OtelRoute.get_router(otel_service), prefix='/api/otel')
app.include_router(HealthcheckRoute.get_healthcheck_route())

app.add_exception_handler(ModelError, model_exception_handler)
app.add_exception_handler(MetricsError, metrics_exception_handler)
app.add_exception_handler(ProjectError, project_exception_handler)
app.add_exception_handler(TraceError, trace_exception_handler)
app.add_exception_handler(ApiKeyError, api_key_exception_handler)
app.add_exception_handler(OtelError, otel_exception_handler)
app.add_exception_handler(SchemaException, schema_exception_handler)
app.add_exception_handler(GenericValidationError, generic_validation_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, internal_exception_handler)
