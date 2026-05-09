from presentation.api.shared.responses import (
    APIErrorResponse,
    APIResponse,
)
from presentation.api.jobs.internal.commands.verify_job.dto import (
    VerifyJobDTO,
    VerifyJobErrorDTO,
)
from presentation.api.jobs.internal.commands.verify_job.literals import (
    VerifyJobResultLiteral,
    VerifyJobErrorResultLiteral,
)

class VerifyJobResponse(APIResponse[VerifyJobDTO]):
    result: VerifyJobResultLiteral

class VerifyJobErrorResponse(APIErrorResponse[VerifyJobErrorDTO]):
    error: VerifyJobErrorResultLiteral