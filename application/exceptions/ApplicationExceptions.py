from application.exceptions.RootExceptions import RetryableException

from domain import FileInfo

class RadarrMovieFileNotUpdated(RetryableException):
        def __init__(self, movie_id: int, expected: FileInfo, actual: FileInfo):
            super().__init__(f"Movie file: {expected.name} has not updated correctly.")
            self.movie_id=movie_id,
            self.expected=expected,
            self.actual=actual,
            