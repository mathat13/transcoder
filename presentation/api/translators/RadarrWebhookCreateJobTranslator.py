from presentation.api.schemas.requests import RadarrWebhookCreateJobRequest
from presentation.api.translators.types import IgnoreReason
from presentation.api.translators.result_types import (TranslatorResult,
                                                       CommandReady,
                                                       Ignored)

from domain import (FileInfo,
                    ExternalMediaIDs,
                    )

from application import CreateJobCommand

class RadarrWebhookCreateJobTranslator:
    @staticmethod
    def translate(request: RadarrWebhookCreateJobRequest) -> TranslatorResult:
            if request.eventType != "Download":
                return Ignored(reason=IgnoreReason.UNSUPPORTED_EVENT_TYPE)
            
            cmd = CreateJobCommand(
                # Map domain exceptions upstream
                # ExternalMediaIDs will be passed to integration by route instead of passed into app
                source_file=FileInfo.from_path(request.movieFile.sourceFile),
                media_ids=ExternalMediaIDs.from_radarr(radarr_id=request.movie.id)
            )

            return CommandReady(command=cmd)