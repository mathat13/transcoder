from typing import Protocol
from uuid import UUID

class JellyfinAPIAdapter(Protocol):
    def refresh_library(self, idempotency_key: UUID) -> None:
        ...
