from typing import Literal

from presentation.api.use_cases.common.response_envelopes import APISuccessResponse
from presentation.api.use_cases.jobs.internal.queries.projections.job_summary.projection import JobSummaryDTO

GetJobByIDResultLiteral = Literal[
    "job_found",
    "job_not_found",
]

class GetJobByIDSuccessResponse(APISuccessResponse[JobSummaryDTO]):
    result: GetJobByIDResultLiteral