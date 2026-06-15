from typing import BinaryIO, Protocol


class StorageClient(Protocol):
    def upload_fileobj(self, file_obj: BinaryIO, key: str, metadata: dict) -> str:
        ...

    def object_exists(self, bucket: str, key: str) -> bool:
        ...

    def get_uri_scheme(self) -> str:
        ...

    def get_spark_uri_scheme(self) -> str:
        ...

    def get_bucket_name(self) -> str:
        ...


class S3StorageClient:
    def __init__(self, s3_client, bucket_name: str):
        self._s3_client = s3_client
        self._bucket_name = bucket_name

    def upload_fileobj(self, file_obj: BinaryIO, key: str, metadata: dict) -> str:
        self._s3_client.upload_fileobj(
            file_obj,
            self._bucket_name,
            key,
            ExtraArgs={'Metadata': metadata},
        )
        return f's3://{self._bucket_name}/{key}'

    def object_exists(self, bucket: str, key: str) -> bool:
        self._s3_client.head_object(Bucket=bucket, Key=key)
        return True  # raises ClientError if not found

    def get_uri_scheme(self) -> str:
        return 's3'

    def get_spark_uri_scheme(self) -> str:
        return 's3a'

    def get_bucket_name(self) -> str:
        return self._bucket_name


class GCSStorageClient:
    def __init__(self, gcs_config):
        from google.cloud import storage

        if gcs_config.google_application_credentials:
            self._client = storage.Client.from_service_account_json(
                gcs_config.google_application_credentials,
                project=gcs_config.gcs_project_id or None,
            )
        else:
            # Workload Identity / ADC — no credentials needed
            self._client = storage.Client(project=gcs_config.gcs_project_id or None)

        self._bucket_name = gcs_config.gcs_bucket_name
        self._bucket = self._client.bucket(self._bucket_name)

    def upload_fileobj(self, file_obj: BinaryIO, key: str, metadata: dict) -> str:
        blob = self._bucket.blob(key)
        blob.metadata = metadata
        blob.upload_from_file(file_obj)
        return f'gs://{self._bucket_name}/{key}'

    def object_exists(self, bucket: str, key: str) -> bool:
        return self._client.bucket(bucket).blob(key).exists()

    def get_uri_scheme(self) -> str:
        return 'gs'

    def get_spark_uri_scheme(self) -> str:
        return 'gs'

    def get_bucket_name(self) -> str:
        return self._bucket_name
