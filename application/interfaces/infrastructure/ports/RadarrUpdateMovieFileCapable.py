from typing import Protocol

from domain import (
    ExternalMediaIDs,
    OperationContext,
    FileInfo,
)

class UpdateMovieFileCapable(Protocol):
    def get_moviefile(self, media_identifiers: ExternalMediaIDs, context: OperationContext) -> FileInfo:
        ...

    def rescan_movie(self, media_identifiers: ExternalMediaIDs, context: OperationContext) -> None:
        ...

    