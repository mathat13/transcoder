# External Media bounded context

from dataclasses import dataclass

@dataclass(frozen=True)
class ExternalMediaIDs():
    radarr_movie_id: int

    # Required for storing composite of object in sqlalchemy
    def __composite_values__(self):
        return (self.radarr_movie_id,)
    
    @classmethod
    def create(cls, radarr_id: int) -> "ExternalMediaIDs":
        return cls(
            radarr_movie_id=radarr_id
        )
