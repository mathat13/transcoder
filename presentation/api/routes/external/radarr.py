from fastapi import Depends

from presentation.api.presenters.create_job import CreateJobResultPresenter
from presentation.api.schemas.responses import CreateJobResponse
from presentation.api.schemas.requests import RadarrWebhookCreateJobRequest
from presentation.api.translators.RadarrWebhookCreateJobTranslator import RadarrWebhookCreateJobTranslator
from presentation.api.routers import jobs_router as router
from presentation.api.translators.result_types import *
from presentation.api.dependencies import (
    get_job_service,
    build_operation_context,
)

from application import JobService
from domain import OperationContext

@router.post("/create/webhook/radarr", response_model=CreateJobResponse)
def create_job(
    request: RadarrWebhookCreateJobRequest,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    
    result = RadarrWebhookCreateJobTranslator.translate(request=request)

    match result:
        case Ignored(reason=reason):
            return {
                "status": "ignored",
                "reason": reason.value
                }
        case CommandReady():
            return CreateJobResultPresenter.present_create_job(
                service.create_job(cmd=result.command, ctx=ctx)
            )