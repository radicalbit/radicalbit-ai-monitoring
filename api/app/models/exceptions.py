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


class TraceError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class TraceNotFoundError(TraceError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message, self.status_code)


class TraceSortColumnError(TraceError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message, self.status_code)


def trace_exception_handler(_, err: TraceError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


class OtelError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class OtelUnauthorizedError(OtelError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(self.message, self.status_code)


class OtelInternalError(OtelError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, self.status_code)


def otel_exception_handler(_, err: OtelError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


class GenericValidationError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class TimestampsRangeError(GenericValidationError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        super().__init__(self.message, self.status_code)


def generic_validation_exception_handler(_, err: GenericValidationError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


class ProjectError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class ProjectInternalError(ProjectError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, self.status_code)


class ProjectNotFoundError(ProjectError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message, self.status_code)


class ApiKeyError(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message, self.status_code)


class ApiKeyInternalError(ApiKeyError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, self.status_code)


class ApiKeyNotFoundError(ApiKeyError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message, self.status_code)


class ExistingApiKeyError(ApiKeyError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message, self.status_code)


class LastApiKeyError(ApiKeyError):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message, self.status_code)


def api_key_exception_handler(_, err: ApiKeyError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


def project_exception_handler(_, err: ProjectError):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


def schema_exception_handler(_, err: SchemaException):
    if err.status_code >= 500:
        logger.error(err.message)
    else:
        logger.warning(err.message)
    return JSONResponse(
        status_code=err.status_code,
        content=jsonable_encoder(ErrorOut(err.message)),
    )


def reformat_validation_error_message(err: RequestValidationError):
    error_messages = [pydantic_error['msg'] for pydantic_error in err.errors()]
    return '; '.join(error_messages)


def request_validation_exception_handler(_, err: RequestValidationError):
    reformatted_message = reformat_validation_error_message(err)
    logger.error(
        'A validation error has been raised with message [%s]',
        reformatted_message,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(ErrorOut(reformatted_message)),
    )


def internal_exception_handler(_, exc: Exception) -> JSONResponse:
    logger.error('Internal error occurred [%s]', exc)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ErrorOut(f'Internal server error occurred {exc}')),
    )
