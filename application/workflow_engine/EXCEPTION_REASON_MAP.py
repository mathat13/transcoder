from application.exceptions.ServiceExceptions import *
from application.workflow_engine.FailureReason import FailureReason

EXCEPTION_REASON_MAP: dict[type[Exception], FailureReason] = {
    FileSystemIOError: FailureReason.FILESYSTEM_IO,
    FileSystemDestinationExistsButDifferentFile: FailureReason.FILESYSTEM_LOGIC,
    FileSystemSourceFileIsDirectory: FailureReason.FILESYSTEM_LOGIC,
    FileSystemFileMissing: FailureReason.FILESYSTEM_LOGIC,
    APIServiceRetryableException: FailureReason.API_CALL_FAILURE,
    APIServiceTerminalException: FailureReason.API_CALL_FAILURE,
    }