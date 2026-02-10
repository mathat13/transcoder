from typing import Protocol

class FileDeletionCapable(Protocol):
    def delete(self, file: str) -> None:
        ...
