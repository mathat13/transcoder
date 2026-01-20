from typing import Protocol
from uuid import UUID

from domain import ExternalMediaIDs

class SonarrAPIAdapter(Protocol):
    def rescan_episode(self, episode_id: ExternalMediaIDs, idempotency_key: UUID) -> None:
        ...

    def get_episode(self, episode_id: ExternalMediaIDs, idempotency_key: UUID) -> None:
        ...