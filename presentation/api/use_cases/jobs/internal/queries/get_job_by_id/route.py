from fastapi import Depends
from uuid import UUID

from presentation.api.use_cases.jobs.internal.queries.get_job_by_id.egress.presenter import GetJobByIDPresenter
from presentation.api.use_cases.jobs.internal.queries.get_job_by_id.egress.responses.success.response import GetJobByIDSuccessResponse
from presentation.api.use_cases.dependencies import (
    get_job_service,
    build_operation_context,
)
from presentation.api.setup.definitions.routers import jobs_router as router

from domain import OperationContext

from application import JobService

@router.get("/{id}", response_model=GetJobByIDSuccessResponse)
def get_job_by_id(
    id: UUID,
    service: JobService = Depends(get_job_service),
    ctx: OperationContext = Depends(build_operation_context),
):
    result = service.get_job_by_id(id=id, ctx=ctx)
    return GetJobByIDPresenter.present(result=result)

    