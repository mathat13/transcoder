from typing import (
    Literal,
    Union,
)

from presentation.api.use_cases.common.response_envelopes import APIFailureResponse

from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.dtos import JobNotFoundDTO

JobNotFoundResultLiteral = Literal["job_not_found"]

class JobNotFoundResponse(APIFailureResponse[JobNotFoundDTO]):
    error: JobNotFoundResultLiteral

VerifyJobFailureResponse = Union [JobNotFoundResponse]