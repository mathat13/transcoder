from typing import Protocol

class FileExistenceCheckCapable(Protocol):
    def assert_file_existence(self, file: str) -> None:
        ...