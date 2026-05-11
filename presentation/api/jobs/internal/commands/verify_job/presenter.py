from presentation.api.jobs.internal.commands.verify_job.responses.success import VerifyJobSuccessResponse
from presentation.api.jobs.internal.commands.verify_job.responses.failure import VerifyJobFailureResponse

from presentation.api.jobs.internal.commands.verify_job.responses.dtos import (
    VerifyJobSuccessDTO,
    VerifyJobFailureDTO,
)

from application import (
    VerifyJobNotFound,
    VerificationStarted,
    VerifyJobResult,
)

from presentation.api.shared.exceptions import ApplicationFailure

class VerifyJobPresenter:
    @staticmethod
    def present(result: VerifyJobResult) -> VerifyJobSuccessResponse:
        match result:
            case VerificationStarted(job):
                dto = VerifyJobSuccessDTO(
                    id=str(job.id),
                    status=job.status.value,
                )
                return VerifyJobSuccessResponse(
                    result="verification_started",
                    data = dto,
                )
            
            case VerifyJobNotFound(id):
                dto = VerifyJobFailureDTO(
                    id=str(id),
                )
                raise ApplicationFailure(
                    status_code=404,
                    response=VerifyJobFailureResponse(
                        error="job_not_found",
                        data=dto,
                    )
                )