from fastapi import Depends

from presentation.api.presenters.create_job import CreateJobResultPresenter
from presentation.api.presenters.dispatch_job import DispatchJobResultPresenter
from presentation.api.translators.ManualCreateJobTranslator import ManualCreateJobTranslator
from presentation.api.translators.result_types import *
from presentation.api.schemas.responses import (
    DispatchJobResponse,
    CreateJobResponse,
)
from presentation.api.schemas.requests import ManualCreateRequest

from presentation.api.use_cases.dependencies import (
    get_job_service,
    build_operation_context,
)

from presentation.api.setup.definitions.routers import jobs_router as router

from domain import OperationContext

from application import JobService

# Add global exception handler here

@router.post("/dispatch", response_model=DispatchJobResponse)
def dispatch_job(
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    result = service.dispatch_job(ctx=ctx)
    return DispatchJobResultPresenter.present_dispatch_job(result)

@router.post("/create/manual", response_model=CreateJobResponse)
def create_manual_job(
    request: ManualCreateRequest,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    result = ManualCreateJobTranslator.translate(request=request)

    match result:
        case CommandReady():
            return CreateJobResultPresenter.present_create_job(
                service.create_job(cmd=result.command, ctx=ctx)
            )
        # Implement ignore cases if ever needed
