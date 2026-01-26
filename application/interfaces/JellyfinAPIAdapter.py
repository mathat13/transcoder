from typing import Protocol

from domain import OperationContext

class JellyfinAPIAdapter(Protocol):
    def refresh_library(self, context: OperationContext) -> None:
        ...
