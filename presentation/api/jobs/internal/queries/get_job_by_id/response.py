from presentation.api.shared.responses import APIResponse
from presentation.api.jobs.internal.queries.get_job_by_id.dto import JobSummaryDTO
from presentation.api.jobs.internal.queries.get_job_by_id.literals import GetJobByIDResultLiteral

class GetJobByIDResponse(APIResponse[JobSummaryDTO]):
    result: GetJobByIDResultLiteral