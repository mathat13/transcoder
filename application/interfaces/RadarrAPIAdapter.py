from typing import Protocol
from uuid import UUID

from domain import ExternalMediaIDs

class RadarrAPIAdapter(Protocol):
    def rescan_movie(self, movie_id: ExternalMediaIDs, idempotency_key: UUID) -> None:
        ...

    def get_moviefile(self, movie_id: ExternalMediaIDs, idempotency_key: UUID) -> None:
        ...

    