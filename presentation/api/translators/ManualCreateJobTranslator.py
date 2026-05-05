from domain import FileInfo

from presentation.api.schemas.requests import ManualCreateRequest 
from presentation.api.translators.result_types import CommandReady

from application import CreateJobCommand

class ManualCreateJobTranslator:
    @staticmethod
    def translate(request: ManualCreateRequest) -> CommandReady:

        cmd = CreateJobCommand(
            # Map domain exceptions upstream
            source_file=FileInfo.from_path(request.source_file)
            )

        return CommandReady(command=cmd)
