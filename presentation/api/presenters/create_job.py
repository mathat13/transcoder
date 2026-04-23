from presentation.api.schemas.responses import CreateJobResponse

from application import (
    JobCreated,
    CreateJobResult,
)

class CreateJobResultPresenter:
    @staticmethod
    def present_create_job(result: CreateJobResult) -> CreateJobResponse:
        match result:
            case JobCreated(job):
                return CreateJobResponse.from_job(job)
