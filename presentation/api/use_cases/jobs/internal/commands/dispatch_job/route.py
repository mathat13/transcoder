from fastapi import Depends

from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.presenter import DispatchJobPresenter
from presentation.api.translators.result_types import *
from presentation.api.use_cases.jobs.internal.commands.dispatch_job.egress.responses.success.response import DispatchJobSuccessResponse

from presentation.api.use_cases.dependencies import (
    get_job_service,
    build_operation_context,
)
from presentation.api.setup.definitions.routers import jobs_router as router

from domain import OperationContext

from application import JobService

@router.post("/dispatch", response_model=DispatchJobSuccessResponse)
def dispatch_job(
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    result = service.dispatch_job(ctx=ctx)
    return DispatchJobPresenter.present(result)