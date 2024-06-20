class Error(Exception):
    """Base class for all of this library's exceptions."""


class NetworkError(Error):
    """Low-level networking error."""


class ServerError(Error):
    """Error talking to the API."""


class APIError(Error):
    """Error returned from API."""


class ClientError(Error):
    """Error occurend inside the client codebase."""


class UnhandledResponseCode(Error):
    """Error for unhandled response codes to API."""
