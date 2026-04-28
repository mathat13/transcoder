from domain import FileInfo

from presentation.api.schemas.requests import ManualCreateRequest 

from application import CreateJobCommand

class ManualCreateJobTranslator:
    @staticmethod
    def translate(request: ManualCreateRequest) -> CreateJobCommand:
        return CreateJobCommand(
            source_file=FileInfo.from_path(request.source_file)
            )