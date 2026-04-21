from fastapi import HTTPException

from presentation.api.schemas.responses import (VerifyJobResponse,
                                                ErrorResponse,
                                                )
from application import (
    VerifyErrorJobNotFound,
    VerificationStarted,
    VerifyJobResult,
)

class VerifyJobResultPresenter:
    @staticmethod
    def present_verify_job(result: VerifyJobResult):
        match result:
            case VerificationStarted(job):
                return VerifyJobResponse.from_job(job)
            
            case VerifyErrorJobNotFound(job_id):
                raise HTTPException(
                    status_code=404,
                    detail=ErrorResponse(
                        error="job_not_found",
                        job_id=str(job_id)
                    ).model_dump()
                )
