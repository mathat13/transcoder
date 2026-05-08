from fastapi import Depends
from uuid import UUID

from presentation.api.jobs.get_job_by_id.presenter import GetJobByIDResultPresenter
from presentation.api.jobs.get_job_by_id.response import GetJobByIDResponse
from presentation.api.dependencies import (
    get_job_service,
    build_operation_context,
    jobs_router as router,
)

from domain import OperationContext

from application import JobService

@router.get("/{job_id}", response_model=GetJobByIDResponse)
def get_job_by_id(
    job_id: UUID,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    result = service.get_job_by_id(job_id=job_id, ctx=ctx)
    return GetJobByIDResultPresenter.present(result=result)

    