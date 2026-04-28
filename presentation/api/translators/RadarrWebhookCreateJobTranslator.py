from presentation.api.schemas.requests import RadarrWebhookCreateJobRequest

from domain import (FileInfo,
                    ExternalMediaIDs,
                    )

from application import CreateJobCommand

class RadarrWebhookCreateJobTranslator:
    @staticmethod
    def translate(request: RadarrWebhookCreateJobRequest) -> CreateJobCommand:
            return CreateJobCommand(
                    source_file=FileInfo.from_path(request.movieFile.sourceFile),
                    media_ids=ExternalMediaIDs.from_radarr(radarr_id=request.movie.id)
            )