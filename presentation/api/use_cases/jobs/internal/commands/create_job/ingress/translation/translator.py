from domain import FileInfo

from presentation.api.use_cases.jobs.internal.commands.create_job.ingress.request import CreateJobRequest 
from presentation.api.use_cases.jobs.internal.commands.create_job.ingress.translation.results import (
    CommandReady,
    TranslatorResult,
)

from application import CreateJobCommand

class CreateJobTranslator:
    @staticmethod
    def translate(request: CreateJobRequest) -> TranslatorResult:

        cmd = CreateJobCommand(
            # Map domain exceptions upstream
            source_file=FileInfo.from_path(request.source_file)
            )

        return CommandReady(cmd=cmd)
