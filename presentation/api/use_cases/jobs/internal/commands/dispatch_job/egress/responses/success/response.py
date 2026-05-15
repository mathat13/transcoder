from typing import (
    Literal,
    Union,
)

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse
from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.responses.success.dtos import JobDispatchedDTO
from presentation.api.use_cases.common.dtos import EmptyData

JobDispatchedResultLiteral = Literal["job_dispatched"]
NoJobAvailableResultLiteral = Literal["no_job_available"]

class JobDispatchedResponse(APISuccessResponse[JobDispatchedDTO]):
    result: JobDispatchedResultLiteral

class NoJobAvailableResponse(APISuccessResponse[EmptyData]):
    result: NoJobAvailableResultLiteral

DispatchJobSuccessResponse = Union[JobDispatchedResponse, NoJobAvailableResponse]