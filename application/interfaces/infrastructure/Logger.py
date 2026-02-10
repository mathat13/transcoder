from typing import Protocol

class Logger(Protocol):
    def publish_message(self, message: str) -> bool:
        ...

    def publish_error(self, message: str) -> bool:
        ...

    