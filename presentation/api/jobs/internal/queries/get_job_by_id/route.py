from fastapi import Depends
from uuid import UUID

from presentation.api.jobs.internal.queries.get_job_by_id.presenter import GetJobByIDPresenter
from presentation.api.jobs.internal.queries.get_job_by_id.response import GetJobByIDResponse
from presentation.api.dependencies import (
    get_job_service,
    build_operation_context,
)

from presentation.api.routers import jobs_router as router

from domain import OperationContext

from application import JobService

@router.get("/{job_id}", response_model=GetJobByIDResponse)
def get_job_by_id(
    job_id: UUID,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    result = service.get_job_by_id(job_id=job_id, ctx=ctx)
    return GetJobByIDPresenter.present(result=result)

    