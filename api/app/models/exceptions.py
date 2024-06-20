import logging

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core import get_config

logger = logging.getLogger(get_config().log_config.logger_name)


class ErrorOut:
    message: str

    def __init__(self, message):
        self.message = message


class ModelError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class ModelInternalError(ModelError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, self.status_code)


class ModelNotFoundError(ModelError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message, self.status_code)


def model_exception_handler(_, err: ModelError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


class MetricsError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class MetricsNotFoundError(MetricsError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message, self.status_code)


class MetricsBadRequestError(MetricsError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message, self.status_code)


class MetricsInternalError(MetricsError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, self.status_code)


def metrics_exception_handler(_, err: MetricsError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


class SchemaException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message, status_code)


class UnsupportedSchemaException(SchemaException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class InvalidFileException(SchemaException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class FileTooLargeException(SchemaException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)


def schema_exception_handler(_, err: SchemaException):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )
