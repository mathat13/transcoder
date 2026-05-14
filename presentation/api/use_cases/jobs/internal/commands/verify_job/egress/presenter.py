from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.response import VerifyJobSuccessResponse
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.dto import VerifyJobSuccessDTO
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.response import VerifyJobFailureResponse
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.dto import VerifyJobFailureDTO
from presentation.api.use_cases.common.exceptions import ApplicationFailure

from application import (
    VerifyJobNotFound,
    VerificationStarted,
    VerifyJobResult,
)

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
                    data=dto,
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