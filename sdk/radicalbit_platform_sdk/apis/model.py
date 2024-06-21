from radicalbit_platform_sdk.commons import invoke
from radicalbit_platform_sdk.apis import ModelReferenceDataset, ModelCurrentDataset
from radicalbit_platform_sdk.models import (
    ColumnDefinition,
    Granularity,
    ModelDefinition,
    ModelType,
    DataType,
    OutputType,
    ReferenceFileUpload,
    CurrentFileUpload,
    FileReference,
    AwsCredentials,
)
from radicalbit_platform_sdk.errors import ClientError
from botocore.exceptions import ClientError as BotoClientError
from pydantic import ValidationError
from typing import Optional, List
from uuid import UUID
import boto3
import os
import pandas as pd
import requests


class Model:
    def __init__(self, base_url: str, definition: ModelDefinition) -> None:
        self.__base_url = base_url
        self.__uuid = definition.uuid
        self.__name = definition.name
        self.__description = definition.description
        self.__model_type = definition.model_type
        self.__data_type = definition.data_type
        self.__granularity = definition.granularity
        self.__features = definition.features
        self.__target = definition.target
        self.__timestamp = definition.timestamp
        self.__outputs = definition.outputs
        self.__frameworks = definition.frameworks
        self.__algorithm = definition.algorithm

    def uuid(self) -> UUID:
        return self.__uuid

    def name(self) -> str:
        return self.__name

    def description(self) -> Optional[str]:
        return self.__description

    def model_type(self) -> ModelType:
        return self.__model_type

    def data_type(self) -> DataType:
        return self.__data_type

    def granularity(self) -> Granularity:
        return self.__granularity

    def features(self) -> List[ColumnDefinition]:
        return self.__features

    def target(self) -> ColumnDefinition:
        return self.__target

    def timestamp(self) -> ColumnDefinition:
        return self.__timestamp

    def outputs(self) -> OutputType:
        return self.__outputs

    def frameworks(self) -> Optional[str]:
        return self.__frameworks

    def algorithm(self) -> Optional[str]:
        return self.__algorithm

    def delete(self) -> None:
        """Delete the actual `Model` from the platform

        :return: None
        """
        invoke(
            method="DELETE",
            url=f"{self.__base_url}/api/models/{str(self.__uuid)}",
            valid_response_code=200,
            func=lambda _: None,
        )

    def load_reference_dataset(
        self,
        file_name: str,
        bucket: str,
        object_name: Optional[str] = None,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ",",
    ) -> ModelReferenceDataset:
        """Upload reference dataset to an S3 bucket and then bind it inside the platform.

        Raises `ClientError` in case S3 upload fails.

        :param file_name: The name of the reference file.
        :param bucket: The name of the S3 bucket.
        :param object_name: The optional name of the object uploaded to S3. Default value is None.
        :param aws_credentials: AWS credentials used to connect to S3 bucket. Default value is None.
        :param separator: Optional value to define separator used inside CSV file. Default falue is ","
        :return: An instance of `ModelReferenceDataset` representing the reference dataset
        """

        file_headers = pd.read_csv(
            file_name, nrows=0, delimiter=separator
        ).columns.tolist()

        required_headers = self.__required_headers()

        if set(required_headers).issubset(file_headers):
            if object_name is None:
                object_name = f"{self.__uuid}/reference/{os.path.basename(file_name)}"

            try:
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=(
                        None
                        if aws_credentials is None
                        else aws_credentials.access_key_id
                    ),
                    aws_secret_access_key=(
                        None
                        if aws_credentials is None
                        else aws_credentials.secret_access_key
                    ),
                    region_name=(
                        None
                        if aws_credentials is None
                        else aws_credentials.default_region
                    ),
                )

                s3_client.upload_file(
                    file_name,
                    bucket,
                    object_name,
                    ExtraArgs={
                        "Metadata": {
                            "model_uuid": str(self.__uuid),
                            "model_name": self.__name,
                            "file_type": "reference",
                        }
                    },
                )
            except BotoClientError as e:
                raise ClientError(
                    f"Unable to upload file {file_name} to remote storage: {e}"
                )
            return self.__bind_reference_dataset(
                f"s3://{bucket}/{object_name}", separator
            )
        else:
            raise ClientError(
                f"File {file_name} not contains all defined columns: {required_headers}"
            )

    def bind_reference_dataset(
        self,
        dataset_url: str,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ",",
    ) -> ModelReferenceDataset:
        """Bind an existing reference dataset file already uploded to S3 to a `Model`

        :param dataset_url: The url of the file already uploaded inside S3
        :param aws_credentials: AWS credentials used to connect to S3 bucket. Default value is None.
        :param separator: Optional value to define separator used inside CSV file. Default falue is ","
        :return: An instance of `ModelReferenceDataset` representing the reference dataset
        """

        url_parts = dataset_url.replace("s3://", "").split("/")

        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=(
                    None if aws_credentials is None else aws_credentials.access_key_id
                ),
                aws_secret_access_key=(
                    None
                    if aws_credentials is None
                    else aws_credentials.secret_access_key
                ),
                region_name=(
                    None if aws_credentials is None else aws_credentials.default_region
                ),
            )

            chunks_iterator = s3_client.get_object(
                Bucket=url_parts[0], Key="/".join(url_parts[1:])
            )["Body"].iter_chunks()

            chunks = ""
            for c in (chunk for chunk in chunks_iterator if "\n" not in chunks):
                chunks += c.decode("UTF-8")

            file_headers = chunks.split("\n")[0].split(separator)

            required_headers = self.__required_headers()

            if set(required_headers).issubset(file_headers):
                return self.__bind_reference_dataset(dataset_url, separator)
            else:
                raise ClientError(
                    f"File {dataset_url} not contains all defined columns: {required_headers}"
                )
        except BotoClientError as e:
            raise ClientError(
                f"Unable to get file {dataset_url} from remote storage: {e}"
            )

    def load_current_dataset(
        self,
        file_name: str,
        bucket: str,
        correlation_id_column: str,
        object_name: Optional[str] = None,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ",",
    ) -> ModelCurrentDataset:
        """Upload current dataset to an S3 bucket and then bind it inside the platform.

        Raises `ClientError` in case S3 upload fails.

        :param file_name: The name of the reference file.
        :param bucket: The name of the S3 bucket.
        :param correlation_id_column: The name of the column used for correlation id
        :param object_name: The optional name of the object uploaded to S3. Default value is None.
        :param aws_credentials: AWS credentials used to connect to S3 bucket. Default value is None.
        :param separator: Optional value to define separator used inside CSV file. Default falue is ","
        :return: An instance of `ModelReferenceDataset` representing the reference dataset
        """

        file_headers = pd.read_csv(
            file_name, nrows=0, delimiter=separator
        ).columns.tolist()

        required_headers = self.__required_headers()
        required_headers.append(correlation_id_column)
        required_headers.append(self.__timestamp.name)

        if set(required_headers).issubset(file_headers):
            if object_name is None:
                object_name = f"{self.__uuid}/current/{os.path.basename(file_name)}"

            try:
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=(
                        None
                        if aws_credentials is None
                        else aws_credentials.access_key_id
                    ),
                    aws_secret_access_key=(
                        None
                        if aws_credentials is None
                        else aws_credentials.secret_access_key
                    ),
                    region_name=(
                        None
                        if aws_credentials is None
                        else aws_credentials.default_region
                    ),
                )

                s3_client.upload_file(
                    file_name,
                    bucket,
                    object_name,
                    ExtraArgs={
                        "Metadata": {
                            "model_uuid": str(self.__uuid),
                            "model_name": self.__name,
                            "file_type": "reference",
                        }
                    },
                )
            except BotoClientError as e:
                raise ClientError(
                    f"Unable to upload file {file_name} to remote storage: {e}"
                )
            return self.__bind_current_dataset(
                f"s3://{bucket}/{object_name}", separator, correlation_id_column
            )
        else:
            raise ClientError(
                f"File {file_name} not contains all defined columns: {required_headers}"
            )

    def bind_current_dataset(
        self,
        dataset_url: str,
        correlation_id_column: str,
        aws_credentials: Optional[AwsCredentials] = None,
        separator: str = ",",
    ) -> ModelCurrentDataset:
        """Bind an existing current dataset file already uploded to S3 to a `Model`

        :param dataset_url: The url of the file already uploaded inside S3
        :param correlation_id_column: The name of the column used for correlation id
        :param aws_credentials: AWS credentials used to connect to S3 bucket. Default value is None.
        :param separator: Optional value to define separator used inside CSV file. Default falue is ","
        :return: An instance of `ModelReferenceDataset` representing the reference dataset
        """

        url_parts = dataset_url.replace("s3://", "").split("/")

        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=(
                    None if aws_credentials is None else aws_credentials.access_key_id
                ),
                aws_secret_access_key=(
                    None
                    if aws_credentials is None
                    else aws_credentials.secret_access_key
                ),
                region_name=(
                    None if aws_credentials is None else aws_credentials.default_region
                ),
            )

            chunks_iterator = s3_client.get_object(
                Bucket=url_parts[0], Key="/".join(url_parts[1:])
            )["Body"].iter_chunks()

            chunks = ""
            for c in (chunk for chunk in chunks_iterator if "\n" not in chunks):
                chunks += c.decode("UTF-8")

            file_headers = chunks.split("\n")[0].split(separator)

            required_headers = self.__required_headers()
            required_headers.append(correlation_id_column)
            required_headers.append(self.__timestamp.name)

            if set(required_headers).issubset(file_headers):
                return self.__bind_current_dataset(
                    dataset_url, separator, correlation_id_column
                )
            else:
                raise ClientError(
                    f"File {dataset_url} not contains all defined columns: {required_headers}"
                )
        except BotoClientError as e:
            raise ClientError(
                f"Unable to get file {dataset_url} from remote storage: {e}"
            )

    def __bind_reference_dataset(
        self,
        dataset_url: str,
        separator: str,
    ) -> ModelReferenceDataset:
        def __callback(response: requests.Response) -> ModelReferenceDataset:
            try:
                response = ReferenceFileUpload.model_validate(response.json())
                return ModelReferenceDataset(
                    self.__base_url, self.__uuid, self.__model_type, response
                )
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        file_ref = FileReference(file_url=dataset_url, separator=separator)

        return invoke(
            method="POST",
            url=f"{self.__base_url}/api/models/{str(self.__uuid)}/reference/bind",
            valid_response_code=200,
            func=__callback,
            data=file_ref.model_dump_json(),
        )

    def __bind_current_dataset(
        self,
        dataset_url: str,
        separator: str,
        correlation_id_column: str,
    ) -> ModelCurrentDataset:
        def __callback(response: requests.Response) -> ModelCurrentDataset:
            try:
                response = CurrentFileUpload.model_validate(response.json())
                return ModelCurrentDataset(
                    self.__base_url, self.__uuid, self.__model_type, response
                )
            except ValidationError as _:
                raise ClientError(f"Unable to parse response: {response.text}")

        file_ref = FileReference(
            file_url=dataset_url,
            separator=separator,
            correlation_id_column=correlation_id_column,
        )

        return invoke(
            method="POST",
            url=f"{self.__base_url}/api/models/{str(self.__uuid)}/current/bind",
            valid_response_code=200,
            func=__callback,
            data=file_ref.model_dump_json(),
        )

    def __required_headers(self) -> List[str]:
        model_columns = self.__features + self.__outputs.output
        model_columns.append(self.__target)
        return [model_column.name for model_column in model_columns]
