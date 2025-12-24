from typing import Protocol

class JellyfinAPIAdapter(Protocol):
    def refresh_library(self) -> None:
        ...
