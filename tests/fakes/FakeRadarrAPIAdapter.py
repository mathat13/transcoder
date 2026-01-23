from domain import (
    ExternalMediaIDs,
    FileInfo,
)

class FakeRadarrAPIAdapter:
    def __init__(self):
        self.moviefiles: dict[int, str] = {}
        self.rescan_called_with: list[int] = []

    def _add_movie(self, movie_info: ExternalMediaIDs, file: FileInfo):
        """Test helper: preload adapter state."""
        self.moviefiles[movie_info.radarr_movie_id] = file

    def get_moviefile(self, movie_info: ExternalMediaIDs):
        return self.moviefiles[movie_info.radarr_movie_id]

    def rescan_movie(self, movie_info: ExternalMediaIDs):
        self.rescan_called_with.append(movie_info.radarr_movie_id)