from application.exceptions.RootException import RootException

from domain import FileInfo

class ApplicationException(RootException):
    """Base class for failures caused by internal state not matching expected internal state."""

class RadarrMovieFileNotUpdated(ApplicationException):
        def __init__(self, movie_id: int, expected: FileInfo, actual: FileInfo):
            super().__init__(f"Movie file: {expected.name} has not updated correctly.")
            self.movie_id=movie_id,
            self.expected=expected,
            self.actual=actual,
            self.retryable=True
            