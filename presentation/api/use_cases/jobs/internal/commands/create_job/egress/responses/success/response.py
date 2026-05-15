from typing import (
    Literal,
    Union,
)

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse
from presentation.api.use_cases.jobs.internal.commands.create_job.egress.responses.success.dtos import JobCreatedDTO

JobCreatedResultLiteral = Literal["job_created"]

class JobCreatedResponse(APISuccessResponse[JobCreatedDTO]):
    result: JobCreatedResultLiteral

CreateJobSuccessResponse = Union[JobCreatedResponse]