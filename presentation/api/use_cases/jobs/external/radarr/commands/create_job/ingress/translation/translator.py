from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.request import CreateJobRequest
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.types import IgnoreReason
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import (
    TranslatorResult,
    CommandReady,
    Ignored
)

from domain import (FileInfo,
                    ExternalMediaIDs,
                    )

from application import CreateJobCommand

class CreateJobTranslator:
    @staticmethod
    def translate(request: CreateJobRequest) -> TranslatorResult:
            if request.eventType != "Download":
                return Ignored(reason=IgnoreReason.UNSUPPORTED_EVENT_TYPE)
            
            cmd = CreateJobCommand(
                # Map domain exceptions upstream
                # ExternalMediaIDs will be passed to integration by route instead of passed into app
                source_file=FileInfo.from_path(request.movieFile.sourceFile),
                media_ids=ExternalMediaIDs.from_radarr(radarr_id=request.movie.id)
            )

            return CommandReady(cmd=cmd)