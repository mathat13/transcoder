from typing import (
    Literal,
    Union
)

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse
from presentation.api.use_cases.common.dtos import EmptyData
from presentation.api.use_cases.jobs.internal.queries.projections.job_summary.projection import JobSummaryDTO

JobFoundResultLiteral = Literal["job_found"]
JobNotFoundResultLiteral = Literal["job_not_found"]

class JobFoundResponse(APISuccessResponse[JobSummaryDTO]):
    result: JobFoundResultLiteral

class JobNotFoundResponse(APISuccessResponse[EmptyData]):
    result: JobNotFoundResultLiteral

GetJobByIDSuccessResponse = Union[JobFoundResponse, JobNotFoundResponse]
