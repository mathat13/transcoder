from typing import Protocol

from domain import FileInfo

class Filesystem(Protocol):
    def exists(self, file: FileInfo) -> bool:
        ...