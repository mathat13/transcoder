from typing import Protocol

class HardlinkCapable(Protocol):
    def hardlink(self, source_file: str, destination: str) -> None:
        ...