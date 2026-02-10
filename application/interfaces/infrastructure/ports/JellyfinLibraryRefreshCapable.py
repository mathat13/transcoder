from typing import Protocol

from domain import OperationContext

class JellyfinLibraryRefreshCapable(Protocol):
    def refresh_library(self, context: OperationContext) -> None:
        ...
