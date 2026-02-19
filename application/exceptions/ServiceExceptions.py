from application.exceptions.RootException import RootException

from domain import FileInfo

class ServiceException(RootException):
    """Base class for failures caused by external services."""
    
class APICallException(ServiceException):
    """Base class for API call-related failures."""

class APIServiceException(APICallException):
    def __init__(self, service: str, status_code: int, retryable: bool, detail: str | dict | None):
        super().__init__(f"{service} API failed with status {status_code}")
        self.service = service
        self.status_code = status_code
        self.retryable = retryable
        self.detail = detail

class FileSystemException(ServiceException):
    """Base class for filesystem-related failures."""

class SourceFileMissing(FileSystemException):
    def __init__(self, file: str):
        super().__init__(f"Source file does not exist: {file}")
        self.file = FileInfo(file)
        self.retryable = False

class SourceFileIsDirectory(FileSystemException):
    def __init__(self, operation: str, file: str):
        super().__init__(f"Source file is a directory, cannot proceed with operation: {operation} -> {file}")
        self.operation = operation
        self.file = FileInfo(file)
        self.retryable = False

class DestinationExistsButDifferentFile(FileSystemException):
    def __init__(self, file: str):
        super().__init__(f"Destination exists but is a different file: {file}")
        self.file = FileInfo(file)
        self.retryable = False

class FileSystemIOError(FileSystemException):
    def __init__(self, operation: str, file: str, original: Exception):
        super().__init__(f"Filesystem error during {operation} on {file}")
        self.operation = operation
        self.file = FileInfo(file)
        self.original = original
        self.retryable = True

