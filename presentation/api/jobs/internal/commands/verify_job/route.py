from fastapi import Depends
from uuid import UUID

from presentation.api.jobs.internal.commands.verify_job.presenter import VerifyJobPresenter
from presentation.api.translators.result_types import *
from presentation.api.jobs.internal.commands.verify_job.response import VerifyJobResponse

from presentation.api.dependencies import (
    get_job_service,
    build_operation_context,
)

from presentation.api.routers import jobs_router as router

from domain import OperationContext

from application import JobService

@router.post("/{job_id}/verify", response_model=VerifyJobResponse)
def verify_job(
    job_id: UUID,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    
    result = service.verify_job(job_id=job_id, ctx=ctx)
    return VerifyJobPresenter.present(result)