from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.responses.success.response import (
    DispatchJobSuccessResponse,
    NoJobAvailableResponse,
    JobDispatchedResponse,
)
from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.responses.success.dtos import JobDispatchedDTO

from application import (
    NoJobAvailable,
    JobDispatched,
    DispatchJobResult,
)

class DispatchJobPresenter:
    @staticmethod
    def present(result: DispatchJobResult) -> DispatchJobSuccessResponse:
        match result:
            case JobDispatched(job):
                dto = JobDispatchedDTO(
                    id=str(job.id),
                    source_file=str(job.source_file.path),
                    transcode_output_file=str(job.transcode_output_file.path),
                )
                return JobDispatchedResponse(
                    result="job_dispatched",
                    data=dto,
                )
            
            case NoJobAvailable():
                return NoJobAvailableResponse(
                    result="no_job_available",
                )