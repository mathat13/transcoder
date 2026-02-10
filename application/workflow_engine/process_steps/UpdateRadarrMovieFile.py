from application.workflow_engine.process_contexts.ProcessContext import ProcessContext
from application.interfaces.workflow_engine.ProcessStep import ProcessStep
from application.exceptions.ApplicationExceptions import RadarrMovieFileNotUpdated
from application.interfaces.infrastructure.ports.RadarrUpdateMovieFileCapable import RadarrUpdateMovieFileCapable

class UpdateRadarrMovieFile(ProcessStep):
    radarr: RadarrUpdateMovieFileCapable

    def __init__(self, radarr):
        self.radarr = radarr

    @property
    def name(self) -> str:
        """Step name (used for observability)."""
        return "Update Radarr movie file"

    def execute(self, process_context: "ProcessContext") -> None:
        """
        Execute the step.

        Raises:
            Exception on failure (expected and mapped upstream).
        """
        # rescan movie file to pick up new transcode
        self.radarr.rescan_movie(context=process_context.operation_context)

        # Perform twice for good measure (advised by users)
        self.radarr.rescan_movie(context=process_context.operation_context)

        # Get new movie file
        movie_file = self.radarr.get_moviefile(media_identifiers=process_context.media.media_ids,
                                                context=process_context.operation_context)

        if movie_file != process_context.files.transcode_file:
            raise RadarrMovieFileNotUpdated(
                movie_id=process_context.media.media_ids.radarr_movie_id,
                expected=process_context.files.transcode_file,
                actual=movie_file,
            )
