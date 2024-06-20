from enum import Enum


class JobStatus(str, Enum):
    IMPORTING = "IMPORTING"
    SUCCEEDED = "SUCCEEDED"
    ERROR = "ERROR"
