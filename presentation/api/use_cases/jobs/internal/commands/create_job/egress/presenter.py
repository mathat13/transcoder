from presentation.api.use_cases.jobs.internal.commands.create_job.egress.responses.success.response import (
    CreateJobSuccessResponse,
    JobCreatedResponse,
)
from presentation.api.use_cases.jobs.internal.commands.create_job.egress.responses.success.dtos import JobCreatedDTO

from application import (
    JobCreatedResult,
    CreateJobResult,
)

class CreateJobPresenter:
    @staticmethod
    def present(result: CreateJobResult) -> CreateJobSuccessResponse:
        match result:
            case JobCreatedResult(job):
                dto = JobCreatedDTO(
                    id=str(job.id),
                    status=job.status.value,
                    source_file=str(job.source_file.path)
                )
                return JobCreatedResponse(
                    result="job_created",
                    data=dto,
                )