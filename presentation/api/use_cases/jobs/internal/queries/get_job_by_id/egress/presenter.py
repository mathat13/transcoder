from presentation.api.use_cases.jobs.internal.queries.get_job_by_id.egress.responses.success.response import (
    GetJobByIDSuccessResponse,
    JobFoundResponse,
    JobNotFoundResponse,
)
from presentation.api.use_cases.jobs.internal.queries.get_job_by_id.egress.responses.success.dtos import JobNotFoundDTO
from presentation.api.use_cases.jobs.internal.queries.projections.job_summary.mapper import JobSummaryMapper

from application.services.jobs.queries.get_job_by_id.results import (
    JobFound,
    JobNotFound,
    GetJobByIDResult,
)

class GetJobByIDPresenter:
    @staticmethod
    def present(result: GetJobByIDResult) -> GetJobByIDSuccessResponse:
        match result:
            case JobFound(job=job):
                dto = JobSummaryMapper.to_job_summary(job=job)
                return JobFoundResponse(
                    result="job_found",
                    data=dto,
                    )
            case JobNotFound():
                dto = JobNotFoundDTO()
                return JobNotFoundResponse(
                    result="job_not_found",
                    data=dto
                    )