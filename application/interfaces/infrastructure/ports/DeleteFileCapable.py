from typing import Protocol

class DeleteFileCapable(Protocol):
    def delete(self, file: str) -> None:
        ...
