import logging

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
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


def request_validation_exception_handler(_, err: RequestValidationError):
    validation_errors = err.errors()
    error_messages = [error['msg'] for error in validation_errors]
    parts = error_messages[0].split(',', 1)
    error_type = parts[0].strip()
    error_message = parts[1].strip() if len(parts) > 1 else ''
    logger.error(
        'A validation error [%s] has been raised with message [%s]',
        error_type,
        error_message,
    )
    return JSONResponse(
        status_code=422,  # https://www.rfc-editor.org/rfc/rfc9110.html#name-422-unprocessable-content
        content=jsonable_encoder(ErrorOut(error_message)),
    )


def internal_exception_handler(_, exc: Exception) -> JSONResponse:
    logger.error('Internal error occurred [%s]', exc)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ErrorOut(f'Internal server error occurred {exc}')),
    )
