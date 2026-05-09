from presentation.api.jobs.internal.queries.get_job_by_id.response import GetJobByIDResponse
from presentation.api.jobs.internal.queries.get_job_by_id.mapper import JobSummaryMapper

from application import (
    GetJobByIDFound,
    GetJobByIDNotFound,
    GetJobByIDResult,
)

class GetJobByIDPresenter:
    @staticmethod
    def present(result: GetJobByIDResult) -> GetJobByIDResponse:
        match result:
            case GetJobByIDFound(job=job):
                dto = JobSummaryMapper.to_job_summary(job=job)
                return GetJobByIDResponse(
                    result="job_found",
                    data=dto,
                    )
            case GetJobByIDNotFound():
                return GetJobByIDResponse(result="job_not_found")