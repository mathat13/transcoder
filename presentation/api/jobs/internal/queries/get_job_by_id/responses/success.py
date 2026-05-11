from typing import Literal

from presentation.api.shared.response_envelopes import APISuccessResponse
from presentation.api.jobs.internal.queries.dtos.job_summary.dto import JobSummaryDTO

GetJobByIDResultLiteral = Literal[
    "job_found",
    "job_not_found",
]
class GetJobByIDSuccessResponse(APISuccessResponse[JobSummaryDTO]):
    result: GetJobByIDResultLiteral