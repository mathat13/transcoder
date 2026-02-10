from domain import (
    ExternalMediaIDs,
    FileInfo,
    OperationContext,
)

from application import RadarrUpdateMovieFileCapable

class FakeRadarrAPIAdapter(RadarrUpdateMovieFileCapable):
    def __init__(self):
        self.moviefiles: dict[int, str] = {}
        self.rescan_called_with: list[int] = []

    def _add_movie(self, media_identifiers: ExternalMediaIDs, file: FileInfo, context: OperationContext):
        """Test helper: preload adapter state."""
        self.moviefiles[media_identifiers.radarr_movie_id] = file

    def get_moviefile(self, media_identifiers: ExternalMediaIDs, context: OperationContext):
        return self.moviefiles[media_identifiers.radarr_movie_id]

    def rescan_movie(self, media_identifiers: ExternalMediaIDs, context: OperationContext):
        self.rescan_called_with.append(media_identifiers.radarr_movie_id)