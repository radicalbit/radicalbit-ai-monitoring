from copy import deepcopy
import datetime
from io import BytesIO
import json
import logging
import pathlib
from typing import List, Optional
from uuid import UUID, uuid4

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, UploadFile
from fastapi_pagination import Page, Params
import pandas as pd
from pydantic import ValidationError
from spark_on_k8s.client import ExecutorInstances, PodResources, SparkOnK8S
from spark_on_k8s.utils.configuration import Configuration

from app.core.config.config import create_secrets, get_config
from app.db.dao.completion_dataset_dao import CompletionDatasetDAO
from app.db.dao.current_dataset_dao import CurrentDatasetDAO
from app.db.dao.reference_dataset_dao import ReferenceDatasetDAO
from app.db.tables.completion_dataset_metrics_table import CompletionDatasetMetrics
from app.db.tables.completion_dataset_table import CompletionDataset
from app.db.tables.current_dataset_metrics_table import CurrentDatasetMetrics
from app.db.tables.current_dataset_table import CurrentDataset
from app.db.tables.reference_dataset_metrics_table import ReferenceDatasetMetrics
from app.db.tables.reference_dataset_table import ReferenceDataset
from app.models.commons.order_type import OrderType
from app.models.completion_response import CompletionResponses
from app.models.dataset_dto import (
    CompletionDatasetDTO,
    CurrentDatasetDTO,
    FileCompletion,
    FileReference,
    ReferenceDatasetDTO,
)
from app.models.dataset_type import DatasetType
from app.models.exceptions import (
    FileTooLargeException,
    InvalidFileException,
    ModelNotFoundError,
)
from app.models.inferred_schema_dto import (
    FieldType,
    InferredSchemaDTO,
    SchemaEntry,
    SupportedTypes,
)
from app.models.job_status import JobStatus
from app.models.model_dto import ModelOut, ModelType
from app.models.spark_app_config import get_spark_app_config
from app.services.model_service import ModelService

logger = logging.getLogger(get_config().log_config.logger_name)


class FileService:
    def __init__(
        self,
        reference_dataset_dao: ReferenceDatasetDAO,
        current_dataset_dao: CurrentDatasetDAO,
        completion_dataset_dao: CompletionDatasetDAO,
        model_service: ModelService,
        s3_client: boto3.client,
        spark_k8s_client: SparkOnK8S,
    ) -> 'FileService':
        self.rd_dao = reference_dataset_dao
        self.cd_dao = current_dataset_dao
        self.completion_dataset_dao = completion_dataset_dao
        self.model_svc = model_service
        self.s3_client = s3_client
        s3_config = get_config().s3_config
        self.bucket_name = s3_config.s3_bucket_name
        self.spark_k8s_client = spark_k8s_client
        logger.info('File Service Initialized.')

    def upload_reference_file(
        self, model_uuid: UUID, csv_file: UploadFile, sep: str = ',', columns=None
    ) -> ReferenceDatasetDTO:
        model_out = self.model_svc.get_model_by_uuid(model_uuid)
        if not model_out:
            logger.error('Model %s not found', model_uuid)
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        if self.rd_dao.get_reference_dataset_by_model_uuid(model_uuid) is not None:
            raise HTTPException(
                status_code=404, detail='A reference file was already loaded'
            )

        if columns is None:
            columns = []

        self.validate_file(csv_file, sep, columns)
        _f_name = csv_file.filename
        _f_uuid = uuid4()
        try:
            file_type = 'reference'
            object_name = f'{str(model_out.uuid)}/{file_type}/{_f_uuid}/{_f_name}'
            path = self._upload_file_to_s3(csv_file, model_out, object_name, file_type)

            inserted_file = self.rd_dao.insert_reference_dataset(
                ReferenceDataset(
                    uuid=_f_uuid,
                    model_uuid=model_uuid,
                    path=path,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    status=JobStatus.IMPORTING,
                )
            )

            logger.debug('File %s has been correctly stored in the db', inserted_file)

            spark_app_config = get_spark_app_config(
                model_out.model_type, DatasetType.REFERENCE
            )
            self.__submit_app(
                app_name=str(model_out.uuid),
                app_path=spark_app_config.app_path,
                app_arguments=[
                    model_out.model_dump_json(),
                    path.replace('s3://', 's3a://'),
                    str(inserted_file.uuid),
                    spark_app_config.metrics_table,
                    spark_app_config.dataset_table,
                ],
            )

            return ReferenceDatasetDTO.from_reference_dataset(inserted_file)

        except NoCredentialsError as nce:
            raise HTTPException(
                status_code=500, detail='S3 credentials not available'
            ) from nce
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def bind_reference_file(
        self, model_uuid: UUID, file_ref: FileReference
    ) -> ReferenceDatasetDTO:
        model_out = self.model_svc.get_model_by_uuid(model_uuid)
        if not model_out:
            logger.error('Model %s not found', model_uuid)
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        if self.rd_dao.get_reference_dataset_by_model_uuid(model_uuid) is not None:
            raise HTTPException(
                status_code=404, detail='A reference file was already loaded'
            )
        try:
            url_parts = file_ref.file_url.replace('s3://', '').split('/')
            # check if file exists in S3 with a HEAD operation.
            # if exists then we could update DB otherwise an exception will be raised
            self.s3_client.head_object(Bucket=url_parts[0], Key='/'.join(url_parts[1:]))

            inserted_file = self.rd_dao.insert_reference_dataset(
                ReferenceDataset(
                    uuid=uuid4(),
                    model_uuid=model_uuid,
                    path=file_ref.file_url,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    status=JobStatus.IMPORTING,
                )
            )
            logger.debug('File %s has been correctly stored in the db', inserted_file)

            spark_config = get_config().spark_config
            self.__submit_app(
                app_name=str(model_out.uuid),
                app_path=spark_config.spark_reference_app_path,
                app_arguments=[
                    model_out.model_dump_json(),
                    file_ref.file_url.replace('s3://', 's3a://'),
                    str(inserted_file.uuid),
                    ReferenceDatasetMetrics.__tablename__,
                    ReferenceDataset.__tablename__,
                ],
            )

            return ReferenceDatasetDTO.from_reference_dataset(inserted_file)

        except NoCredentialsError as nce:
            raise HTTPException(
                status_code=500, detail='S3 credentials not available'
            ) from nce
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise HTTPException(
                    status_code=404, detail=f'File {file_ref.file_url} not exists'
                ) from None
            raise HTTPException(status_code=500, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def upload_current_file(
        self,
        model_uuid: UUID,
        csv_file: UploadFile,
        correlation_id_column: Optional[str] = None,
        sep: str = ',',
        columns=None,
    ) -> CurrentDatasetDTO:
        model_out = self.model_svc.get_model_by_uuid(model_uuid)
        if not model_out:
            logger.error('Model %s not found', model_uuid)
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        reference_dataset = self.rd_dao.get_reference_dataset_by_model_uuid(model_uuid)
        if not reference_dataset:
            logger.error('Reference dataset for model %s not found', model_uuid)
            raise ModelNotFoundError(
                f'Reference dataset for model {model_uuid} not found'
            )
        if model_out.model_type is not ModelType.EMBEDDINGS:
            if columns is None:
                model_columns = model_out.features + model_out.outputs.output
                model_columns.append(model_out.target)
                columns = [model_column.name for model_column in model_columns]

            self.validate_file(csv_file, sep, columns)
        _f_name = csv_file.filename
        _f_uuid = uuid4()
        try:
            file_type = 'current'
            object_name = f'{str(model_out.uuid)}/{file_type}/{_f_uuid}/{_f_name}'
            path = self._upload_file_to_s3(csv_file, model_out, object_name, file_type)

            inserted_file = self.cd_dao.insert_current_dataset(
                CurrentDataset(
                    uuid=_f_uuid,
                    model_uuid=model_uuid,
                    path=path,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    correlation_id_column=correlation_id_column,
                    status=JobStatus.IMPORTING,
                )
            )

            logger.debug('File %s has been correctly stored in the db', inserted_file)

            spark_app_config = get_spark_app_config(
                model_out.model_type, DatasetType.CURRENT
            )
            self.__submit_app(
                app_name=str(model_out.uuid),
                app_path=spark_app_config.app_path,
                app_arguments=[
                    model_out.model_dump_json(),
                    path.replace('s3://', 's3a://'),
                    str(inserted_file.uuid),
                    reference_dataset.path.replace('s3://', 's3a://'),
                    spark_app_config.metrics_table,
                    spark_app_config.dataset_table,
                ],
            )

            return CurrentDatasetDTO.from_current_dataset(inserted_file)

        except NoCredentialsError as nce:
            raise HTTPException(
                status_code=500, detail='S3 credentials not available'
            ) from nce
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def bind_current_file(
        self, model_uuid: UUID, file_ref: FileReference
    ) -> CurrentDatasetDTO:
        model_out = self.model_svc.get_model_by_uuid(model_uuid)
        if not model_out:
            logger.error('Model %s not found', model_uuid)
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        reference_dataset = self.rd_dao.get_reference_dataset_by_model_uuid(model_uuid)
        if not reference_dataset:
            logger.error('Reference dataset for model %s not found', model_uuid)
            raise ModelNotFoundError(
                f'Reference dataset for model {model_uuid} not found'
            )
        try:
            url_parts = file_ref.file_url.replace('s3://', '').split('/')
            # check if file exists in S3 with a HEAD operation.
            # if exists then we could update DB otherwise an exception will be raised
            self.s3_client.head_object(Bucket=url_parts[0], Key='/'.join(url_parts[1:]))

            inserted_file = self.cd_dao.insert_current_dataset(
                CurrentDataset(
                    uuid=uuid4(),
                    model_uuid=model_uuid,
                    path=file_ref.file_url,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    correlation_id_column=file_ref.correlation_id_column,
                    status=JobStatus.IMPORTING,
                )
            )
            logger.debug('File %s has been correctly stored in the db', inserted_file)

            spark_config = get_config().spark_config
            self.__submit_app(
                app_name=str(model_out.uuid),
                app_path=spark_config.spark_current_app_path,
                app_arguments=[
                    model_out.model_dump_json(),
                    file_ref.file_url.replace('s3://', 's3a://'),
                    str(inserted_file.uuid),
                    reference_dataset.path.replace('s3://', 's3a://'),
                    CurrentDatasetMetrics.__tablename__,
                    CurrentDataset.__tablename__,
                ],
            )

            return CurrentDatasetDTO.from_current_dataset(inserted_file)

        except NoCredentialsError as nce:
            raise HTTPException(
                status_code=500, detail='S3 credentials not available'
            ) from nce
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise HTTPException(
                    status_code=404, detail=f'File {file_ref.file_url} not exists'
                ) from None
            raise HTTPException(status_code=500, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def upload_completion_file(
        self,
        model_uuid: UUID,
        json_file: UploadFile,
    ) -> CompletionDatasetDTO:
        model_out = self.model_svc.get_model_by_uuid(model_uuid)
        if not model_out:
            logger.error('Model %s not found', model_uuid)
            raise ModelNotFoundError(f'Model {model_uuid} not found')

        validated_json_file = self.validate_json_file(json_file)
        _f_name = validated_json_file.filename
        _f_uuid = uuid4()
        try:
            file_type = 'completion'
            object_name = f'{str(model_out.uuid)}/{file_type}/{_f_uuid}/{_f_name}'
            path = self._upload_file_to_s3(
                validated_json_file, model_out, object_name, file_type
            )

            inserted_file = self.completion_dataset_dao.insert_completion_dataset(
                CompletionDataset(
                    uuid=_f_uuid,
                    model_uuid=model_uuid,
                    path=path,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    status=JobStatus.IMPORTING,
                )
            )

            logger.debug('File %s has been correctly stored in the db', inserted_file)

            spark_app_config = get_spark_app_config(
                model_out.model_type, DatasetType.COMPLETION
            )
            self.__submit_app(
                app_name=str(model_out.uuid),
                app_path=spark_app_config.app_path,
                app_arguments=[
                    path.replace('s3://', 's3a://'),
                    str(inserted_file.uuid),
                    spark_app_config.metrics_table,
                    spark_app_config.dataset_table,
                ],
            )

            return CompletionDatasetDTO.from_completion_dataset(inserted_file)

        except NoCredentialsError as nce:
            raise HTTPException(
                status_code=500, detail='S3 credentials not available'
            ) from nce
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def bind_completion_file(
        self, model_uuid: UUID, file_completion: FileCompletion
    ) -> CompletionDatasetDTO:
        model_out = self.model_svc.get_model_by_uuid(model_uuid)
        if not model_out:
            logger.error('Model %s not found', model_uuid)
            raise ModelNotFoundError(f'Model {model_uuid} not found')
        try:
            url_parts = file_completion.file_url.replace('s3://', '').split('/')
            self.s3_client.head_object(Bucket=url_parts[0], Key='/'.join(url_parts[1:]))

            inserted_file = self.completion_dataset_dao.insert_completion_dataset(
                CompletionDataset(
                    uuid=uuid4(),
                    model_uuid=model_uuid,
                    path=file_completion.file_url,
                    date=datetime.datetime.now(tz=datetime.UTC),
                    status=JobStatus.IMPORTING,
                )
            )
            logger.debug('File %s has been correctly stored in the db', inserted_file)

            spark_config = get_config().spark_config
            self.__submit_app(
                app_name=str(model_out.uuid),
                app_path=spark_config.spark_completion_app_path,
                app_arguments=[
                    file_completion.file_url.replace('s3://', 's3a://'),
                    str(inserted_file.uuid),
                    CompletionDatasetMetrics.__tablename__,
                    CompletionDataset.__tablename__,
                ],
            )

            return CompletionDatasetDTO.from_completion_dataset(inserted_file)

        except NoCredentialsError as nce:
            raise HTTPException(
                status_code=500, detail='S3 credentials not available'
            ) from nce
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise HTTPException(
                    status_code=404,
                    detail=f'File {file_completion.file_url} not exists',
                ) from None
            raise HTTPException(status_code=500, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def get_all_reference_datasets_by_model_uuid_paginated(
        self,
        model_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[ReferenceDatasetDTO]:
        results: Page[ReferenceDatasetDTO] = (
            self.rd_dao.get_all_reference_datasets_by_model_uuid_paginated(
                model_uuid, params=params, order=order, sort=sort
            )
        )

        _items = [
            ReferenceDatasetDTO.from_reference_dataset(reference_file_upload_result)
            for reference_file_upload_result in results.items
        ]

        return Page.create(items=_items, params=params, total=results.total)

    def get_all_reference_datasets_by_model_uuid(
        self,
        model_uuid: UUID,
    ) -> List[ReferenceDatasetDTO]:
        references = self.rd_dao.get_all_reference_datasets_by_model_uuid(model_uuid)

        return [
            ReferenceDatasetDTO.from_reference_dataset(reference)
            for reference in references
        ]

    def get_all_current_datasets_by_model_uuid_paginated(
        self,
        model_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[CurrentDatasetDTO]:
        results: Page[CurrentDatasetDTO] = (
            self.cd_dao.get_all_current_datasets_by_model_uuid_paginated(
                model_uuid, params=params, order=order, sort=sort
            )
        )

        _items = [
            CurrentDatasetDTO.from_current_dataset(current_dataset)
            for current_dataset in results.items
        ]

        return Page.create(items=_items, params=params, total=results.total)

    def get_all_current_datasets_by_model_uuid(
        self,
        model_uuid: UUID,
    ) -> List[CurrentDatasetDTO]:
        currents = self.cd_dao.get_all_current_datasets_by_model_uuid(model_uuid)
        return [
            CurrentDatasetDTO.from_current_dataset(current_dataset)
            for current_dataset in currents
        ]

    def get_all_completion_datasets_by_model_uuid_paginated(
        self,
        model_uuid: UUID,
        params: Params = Params(),
        order: OrderType = OrderType.ASC,
        sort: Optional[str] = None,
    ) -> Page[CompletionDatasetDTO]:
        results: Page[CompletionDatasetDTO] = (
            self.completion_dataset_dao.get_all_completion_datasets_by_model_uuid_paginated(
                model_uuid, params=params, order=order, sort=sort
            )
        )

        _items = [
            CompletionDatasetDTO.from_completion_dataset(completion_dataset)
            for completion_dataset in results.items
        ]

        return Page.create(items=_items, params=params, total=results.total)

    def get_all_completion_datasets_by_model_uuid(
        self,
        model_uuid: UUID,
    ) -> List[CompletionDatasetDTO]:
        completions = (
            self.completion_dataset_dao.get_all_completion_datasets_by_model_uuid(
                model_uuid
            )
        )
        return [
            CompletionDatasetDTO.from_completion_dataset(completion_dataset)
            for completion_dataset in completions
        ]

    def _upload_file_to_s3(
        self,
        input_file: UploadFile,
        model_out: ModelOut,
        object_name: str,
        file_type: str,
    ):
        self.s3_client.upload_fileobj(
            input_file.file,
            self.bucket_name,
            object_name,
            ExtraArgs={
                'Metadata': {
                    'model_uuid': str(model_out.uuid),
                    'model_name': model_out.name,
                    'file_type': file_type,
                }
            },
        )
        return f's3://{self.bucket_name}/{object_name}'

    @staticmethod
    def infer_schema(csv_file: UploadFile, sep: str = ',') -> InferredSchemaDTO:
        FileService.validate_file(csv_file, sep)
        with csv_file.file as f:
            df = pd.read_csv(f, sep=sep)

        return FileService.schema_from_pandas(df)

    @staticmethod
    def schema_from_pandas(df: pd.DataFrame) -> InferredSchemaDTO:
        data = FileService.cast_datetimes(df)
        # Drop unnamed columns
        data = data.loc[:, ~data.columns.str.contains('Unnamed')]
        return InferredSchemaDTO(
            inferred_schema=[
                SchemaEntry(
                    name=name.strip(),
                    type=SupportedTypes.cast(type),
                    field_type=FieldType.from_supported_type(SupportedTypes.cast(type)),
                )
                for name, type in data.convert_dtypes(infer_objects=True).dtypes.items()
            ]
        )

    @staticmethod
    def cast_datetimes(df: pd.DataFrame) -> pd.DataFrame:
        data = deepcopy(df)
        # Cast string timestamp columns to datetime
        for col in filter(lambda col: data[col].dtype == 'object', data.columns):
            try:
                data[col] = pd.to_datetime(data[col])
                logger.debug('Found timestamp column: %s', col)
            except Exception:  # noqa: PERF203
                pass
        return data

    @staticmethod
    def validate_file(
        csv_file: UploadFile, sep: str = ',', columns: List[str] = []
    ) -> None:
        file_upload_config = get_config().file_upload_config
        _f_name = csv_file.filename
        if csv_file.filename is None or csv_file.size == 0:
            raise InvalidFileException('The file is empty. Please enter a valid file.')
        if csv_file.size is not None and csv_file.size >= file_upload_config.max_bytes:
            raise FileTooLargeException(
                f'File is more thant {file_upload_config.max_mega_bytes}MB'
            )
        if (
            _f_name is not None
            and pathlib.Path(_f_name).suffix
            not in file_upload_config.accepted_file_types
        ):
            raise InvalidFileException(
                f'File has not a valid extension. Valid extensions are: {(*file_upload_config.accepted_file_types,)}'
            )

        df = pd.read_csv(csv_file.file, sep=sep)
        col_errors = [col for col in columns if col not in df.columns]
        if len(col_errors) > 0:
            raise InvalidFileException(
                f'Columns {(*col_errors,)} not found in file {_f_name}'
            )

        csv_file.file.flush()
        csv_file.file.seek(0)

    @staticmethod
    def validate_json_file(json_file: UploadFile):
        try:
            content = json_file.file.read().decode('utf-8')
            json_data = json.loads(content)
            validated_data = CompletionResponses.model_validate(json_data)
            return UploadFile(
                filename=json_file.filename,
                file=BytesIO(validated_data.model_dump_json().encode()),
            )
        except ValidationError as e:
            logger.error('Invalid json file: %s', str(e))
            raise InvalidFileException(f'Invalid json file: {str(e)}') from e
        except Exception as e:
            logger.error('Error while reading the json file: %s', str(e))
            raise InvalidFileException(f'Invalid json file: {str(e)}') from e

    def __submit_app(
        self, app_name: str, app_path: str, app_arguments: List[str]
    ) -> None:
        spark_config = get_config().spark_config
        self.spark_k8s_client.submit_app(
            image=spark_config.spark_image,
            app_path=app_path,
            app_arguments=app_arguments,
            app_name=app_name,
            namespace=spark_config.spark_namespace,
            service_account=spark_config.spark_service_account,
            image_pull_policy=spark_config.spark_image_pull_policy,
            app_waiter='no_wait',
            secret_values=create_secrets(),
            driver_annotations=Configuration.SPARK_ON_K8S_SPARK_DRIVER_ANNOTATIONS,
            executor_annotations=Configuration.SPARK_ON_K8S_SPARK_EXECUTOR_ANNOTATIONS,
            driver_resources=PodResources(
                cpu=Configuration.SPARK_ON_K8S_DRIVER_CPU,
                memory=Configuration.SPARK_ON_K8S_DRIVER_MEMORY,
                memory_overhead=Configuration.SPARK_ON_K8S_DRIVER_MEMORY_OVERHEAD,
            ),
            executor_resources=PodResources(
                cpu=Configuration.SPARK_ON_K8S_EXECUTOR_CPU,
                memory=Configuration.SPARK_ON_K8S_EXECUTOR_MEMORY,
                memory_overhead=Configuration.SPARK_ON_K8S_EXECUTOR_MEMORY_OVERHEAD,
            ),
            executor_instances=ExecutorInstances(
                min=Configuration.SPARK_ON_K8S_EXECUTOR_MIN_INSTANCES,
                max=Configuration.SPARK_ON_K8S_EXECUTOR_MAX_INSTANCES,
                initial=Configuration.SPARK_ON_K8S_EXECUTOR_INITIAL_INSTANCES,
            ),
        )
