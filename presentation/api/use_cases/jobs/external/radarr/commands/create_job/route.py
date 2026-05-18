from fastapi import Depends
from fastapi.responses import JSONResponse

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.egress.presenter import CreateJobPresenter
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.egress.responses.success.response import CreateJobSuccessResponse
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.request import CreateJobRequest
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.translator import CreateJobTranslator
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.translation.results import *
from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.presenter import IngressPresenter
from presentation.api.setup.definitions.routers import jobs_router as router
from presentation.api.use_cases.dependencies import (
    get_job_service,
    build_operation_context,
)

from application import JobService
from domain import OperationContext

@router.post("/create/webhook/radarr", response_model=CreateJobSuccessResponse)
def create_job(
    request: CreateJobRequest,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    
    result = CreateJobTranslator.translate(request=request)

    match result:
        case Deny():
            presentation = IngressPresenter.present(result)

            return JSONResponse(
                status_code=presentation.status_code,
                content=presentation.response.model_dump(),
            )
        
        case Admit(cmd):
            result = service.create_job(cmd=cmd, ctx=ctx)
            return CreateJobPresenter.present(result=result)