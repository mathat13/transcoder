from presentation.api.jobs.internal.commands.verify_job.response import (
    VerifyJobResponse,
    VerifyJobErrorResponse,
)
from presentation.api.jobs.internal.commands.verify_job.dto import (
    VerifyJobDTO,
    VerifyJobErrorDTO,
)

from application import (
    VerifyJobNotFound,
    VerificationStarted,
    VerifyJobResult,
)

from presentation.api.shared.exceptions import APIError

class VerifyJobPresenter:
    @staticmethod
    def present(result: VerifyJobResult) -> VerifyJobResponse:
        match result:
            case VerificationStarted(job):
                dto = VerifyJobDTO(
                    id=str(job.id),
                    status=job.status.value,
                )
                return VerifyJobResponse(
                    result="verification_started",
                    data = dto,
                )
            
            case VerifyJobNotFound(id):
                dto = VerifyJobErrorDTO(
                    id=str(id),
                )
                raise APIError(
                    status_code=404,
                    response=VerifyJobErrorResponse(
                        error="job_not_found",
                        data=dto,
                    )
                )