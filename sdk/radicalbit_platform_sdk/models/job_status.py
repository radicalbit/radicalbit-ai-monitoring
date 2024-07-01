from enum import Enum


class JobStatus(str, Enum):
    IMPORTING = 'IMPORTING'
    SUCCEEDED = 'SUCCEEDED'
    ERROR = 'ERROR'


class JobStatusWithMissingDatasetStatus(str, Enum):
    IMPORTING = JobStatus.IMPORTING
    SUCCEEDED = JobStatus.SUCCEEDED
    ERROR = JobStatus.ERROR
    MISSING_REFERENCE = 'MISSING_REFERENCE'
    MISSING_CURRENT = 'MISSING_CURRENT'
