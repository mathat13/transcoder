from typing import Protocol

from domain import (
    ExternalMediaIDs,
    OperationContext,
    FileInfo,
)

class RadarrAPIAdapter(Protocol):
    def rescan_movie(self, media_identifiers: ExternalMediaIDs, context: OperationContext) -> None:
        ...

    def get_moviefile(self, media_identifiers: ExternalMediaIDs, context: OperationContext) -> FileInfo:
        ...

    