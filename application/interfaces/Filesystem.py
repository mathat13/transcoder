from typing import Protocol

class Filesystem(Protocol):
    def exists(self, path: str) -> bool:
        ...