from typing import Protocol

class SonarrAPIAdapter(Protocol):
    def rescan_episode(self,) -> None:
        ...

    def get_episode(self,) -> None:
        ...