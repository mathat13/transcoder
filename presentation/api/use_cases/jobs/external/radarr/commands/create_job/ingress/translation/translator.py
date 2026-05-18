from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.request import CreateJobRequest
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import (
    TranslatorResult,
    Admit,
    Deny
)

from domain import (FileInfo,
                    ExternalMediaIDs,
                    )

from application import CreateJobCommand

class CreateJobTranslator:
    @staticmethod
    def translate(request: CreateJobRequest) -> TranslatorResult:
            if request.eventType != "Download":
                return Deny(reason="unsupported_event_type")
            
            # For domain exceptions, add try/ except block here to catch expected exceptions and
            # map them to Deny with an IngressNonSuccessReason, then pass back as usual
            # Handled upstream by presenter
            cmd = CreateJobCommand(
                # Map domain exceptions upstream
                # ExternalMediaIDs will be passed to integration by route instead of passed into app
                source_file=FileInfo.from_path(request.movieFile.sourceFile),
                media_ids=ExternalMediaIDs.from_radarr(radarr_id=request.movie.id)
            )

            return Admit(cmd=cmd)