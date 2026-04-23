from presentation.api.schemas.responses import (
    DispatchJobResponse,
    )

from application import (
    DispatchJobNoJobAvailable,
    JobDispatched,
    DispatchJobResult,
)

class DispatchJobResultPresenter:
    @staticmethod
    def present_dispatch_job(result: DispatchJobResult) -> DispatchJobResponse:
        match result:
            case JobDispatched(job):
                return DispatchJobResponse.from_job(job)
            
            case DispatchJobNoJobAvailable():
                return DispatchJobResponse.no_job_available()