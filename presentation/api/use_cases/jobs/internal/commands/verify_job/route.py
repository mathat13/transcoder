from fastapi import Depends
from uuid import UUID

from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.presenter import VerifyJobPresenter
from presentation.api.translators.result_types import *
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.response import VerifyJobSuccessResponse

from presentation.api.use_cases.dependencies import (
    get_job_service,
    build_operation_context,
)

from presentation.api.setup.definitions.routers import jobs_router as router

from domain import OperationContext

from application import JobService

@router.post("/{id}/verify", response_model=VerifyJobSuccessResponse)
def verify_job(
    id: UUID,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    
    result = service.verify_job(id=id, ctx=ctx)
    return VerifyJobPresenter.present(result)