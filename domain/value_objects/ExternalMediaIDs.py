from dataclasses import dataclass

@dataclass(frozen=True)
class ExternalMediaIDs():
    radarr_movie_id: int

    @classmethod
    def create(cls, radarr_id: int) -> "ExternalMediaIDs":
        return cls(
            radarr_movie_id=radarr_id
        )
