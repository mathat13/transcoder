from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.response import (
    VerifyJobSuccessResponse,
    VerificationStartedResponse
    )
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.dtos import VerificationStartedDTO
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.response import JobNotFoundResponse
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.dtos import JobNotFoundDTO
from presentation.api.use_cases.common.exceptions import ApplicationFailure

from application.services.jobs.commands.verify_job.results import (
    JobNotFound,
    VerificationStarted,
    VerifyJobResult,
)

class VerifyJobPresenter:
    @staticmethod
    def present(result: VerifyJobResult) -> VerifyJobSuccessResponse:
        match result:
            case VerificationStarted(job):
                dto = VerificationStartedDTO(
                    id=str(job.id),
                    status=job.status.value,
                )
                return VerificationStartedResponse(
                    result="verification_started",
                    data=dto,
                )
            
            case JobNotFound(id):
                dto = JobNotFoundDTO(
                    id=str(id),
                )
                raise ApplicationFailure(
                    status_code=404,
                    response=JobNotFoundResponse(
                        error="job_not_found",
                        data=dto,
                    )
                )