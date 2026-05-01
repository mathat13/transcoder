from fastapi import Depends
from uuid import UUID

from presentation.api.presenters.create_job import CreateJobResultPresenter
from presentation.api.presenters.verify_job import VerifyJobResultPresenter
from presentation.api.presenters.dispatch_job import DispatchJobResultPresenter
from presentation.api.translators.ManualCreateJobTranslator import ManualCreateJobTranslator
from presentation.api.translators.RadarrWebhookCreateJobTranslator import RadarrWebhookCreateJobTranslator
from presentation.api.schemas.responses import (
    VerifyJobResponse,
    DispatchJobResponse,
    CreateJobResponse,
)
from presentation.api.schemas.requests import (
    ManualCreateRequest,
    RadarrWebhookCreateJobRequest,
)

from presentation.api.dependencies import (
    get_job_service,
    build_operation_context,
    jobs_router as router,
)

from domain import OperationContext

from application import JobService


@router.post("/{job_id}/verify", response_model=VerifyJobResponse)
def verify_job(
    job_id: UUID,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    
    result = service.verify_job(job_id=job_id, ctx=ctx)
    return VerifyJobResultPresenter.present_verify_job(result)

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
    cmd = ManualCreateJobTranslator.translate(request=request)

    result = service.create_job(cmd=cmd, ctx=ctx)
    return CreateJobResultPresenter.present_create_job(result)

