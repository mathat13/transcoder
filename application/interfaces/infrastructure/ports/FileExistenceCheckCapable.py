from typing import Protocol

class FileExistenceCheckCapable(Protocol):
    def is_file(self, file: str) -> bool:
        ...