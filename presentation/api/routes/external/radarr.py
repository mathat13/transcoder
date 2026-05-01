from fastapi import Depends

from presentation.api.presenters.create_job import CreateJobResultPresenter
from presentation.api.schemas.responses import CreateJobResponse
from presentation.api.dependencies import (
    get_job_service,
    build_operation_context,
    jobs_router as router,
)

from integrations import (
    RadarrWebhookCreateJobRequest,
    RadarrWebhookCreateJobTranslator
    )

from application import JobService
from domain import OperationContext

@router.post("/create/webhook/radarr", response_model=CreateJobResponse)
def create_job(
    request: RadarrWebhookCreateJobRequest,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    cmd = RadarrWebhookCreateJobTranslator.translate(request=request)

    result = service.create_job(cmd=cmd, ctx=ctx)

    return CreateJobResultPresenter.present_create_job(result)