from typing import Protocol

class RadarrAPIAdapter(Protocol):
    def rescan_movie(self,) -> None:
        ...

    def get_movie(self,) -> None:
        ...

    