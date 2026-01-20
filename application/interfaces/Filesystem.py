from typing import Protocol

class Filesystem(Protocol):
    def exists(self, file: str) -> bool:
        ...

    def hardlink(self, source_file: str, destination: str) -> None:
        ...

    def delete(self, file: str) -> None:
        ...