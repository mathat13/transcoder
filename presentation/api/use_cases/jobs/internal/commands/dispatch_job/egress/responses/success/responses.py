from pydantic import BaseModel
from typing import (
    Literal,
    Union,
)

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse
from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.responses.success.dtos import (
    JobDispatchedDTO,
    NoJobAvailableDTO,
)

JobDispatchedResultLiteral = Literal["job_dispatched"]
NoJobAvailableResultLiteral = Literal["no_job_available"]

class JobDispatchedResponse(APISuccessResponse[JobDispatchedDTO]):
    result: JobDispatchedResultLiteral

class NoJobAvailableResponse(APISuccessResponse[NoJobAvailableDTO]):
    result: NoJobAvailableResultLiteral

DispatchJobSuccessResponse = Union[JobDispatchedResponse, NoJobAvailableResponse]