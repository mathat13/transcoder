from presentation.api.schemas.responses import ApiResponse
from presentation.api.jobs.get_job_by_id.dto import JobSummaryDTO
from presentation.api.jobs.get_job_by_id.literals import GetJobByIDResultLiteral

class GetJobByIDResponse(ApiResponse[JobSummaryDTO]):
    result: GetJobByIDResultLiteral