from application.exceptions.RootExceptions import (RetryableException,
                                                   TerminalException)

from domain import FileInfo

class APIServiceRetryableException(RetryableException):
    def __init__(self, service: str, status_code: int, detail: str | dict | None):
        super().__init__(f"{service} API failed with status {status_code}")
        self.service = service
        self.status_code = status_code
        self.detail = detail

class APIServiceTerminalException(TerminalException):
    def __init__(self, service: str, status_code: int, detail: str | dict | None):
        super().__init__(f"{service} API failed with status {status_code}")
        self.service = service
        self.status_code = status_code
        self.detail = detail

class FileSystemFileMissing(TerminalException):
    def __init__(self, file: str):
        super().__init__(f"File does not exist: {file}")
        self.file = FileInfo(file)

class FileSystemSourceFileIsDirectory(TerminalException):
    def __init__(self, operation: str, file: str):
        super().__init__(f"Source file is a directory, cannot proceed with operation: {operation} -> {file}")
        self.operation = operation
        self.file = FileInfo(file)

class FileSystemDestinationExistsButDifferentFile(TerminalException):
    def __init__(self, file: str):
        super().__init__(f"Destination exists but is a different file: {file}")
        self.file = FileInfo(file)

class FileSystemIOError(RetryableException):
    def __init__(self, operation: str, file: str, original: Exception):
        super().__init__(f"Filesystem error during {operation} on {file}")
        self.operation = operation
        self.file = FileInfo(file)
        self.original = original

