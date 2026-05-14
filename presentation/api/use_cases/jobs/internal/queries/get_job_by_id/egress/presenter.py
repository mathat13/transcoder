from presentation.api.use_cases.jobs.internal.queries.get_job_by_id.egress.responses.success import GetJobByIDSuccessResponse
from presentation.api.use_cases.jobs.internal.queries.projections.job_summary.mapper import JobSummaryMapper

from application import (
    GetJobByIDFound,
    GetJobByIDNotFound,
    GetJobByIDResult,
)

class GetJobByIDPresenter:
    @staticmethod
    def present(result: GetJobByIDResult) -> GetJobByIDSuccessResponse:
        match result:
            case GetJobByIDFound(job=job):
                dto = JobSummaryMapper.to_job_summary(job=job)
                return GetJobByIDSuccessResponse(
                    result="job_found",
                    data=dto,
                    )
            case GetJobByIDNotFound():
                return GetJobByIDSuccessResponse(result="job_not_found")