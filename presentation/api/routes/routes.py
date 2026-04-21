from fastapi import APIRouter, Depends
from uuid import UUID

from presentation.api.presenters.verify_job import VerifyJobResultPresenter
from presentation.api.presenters.dispatch_job import DispatchJobResultPresenter
from presentation.api.schemas.responses import (
    VerifyJobResponse,
    DispatchJobResponse,
)
from presentation.api.dependencies import get_job_service

from application import JobService

router = APIRouter(prefix="/jobs")

@router.post("/{job_id}/verify", response_model=VerifyJobResponse)
def verify_job(
    job_id: UUID,
    service: JobService = Depends(get_job_service)
):
    result = service.verify_job(job_id)
    return VerifyJobResultPresenter.present_verify_job(result)

@router.post("/dispatch", response_model=DispatchJobResponse)
def dispatch_job(
    service: JobService = Depends(get_job_service)
):
    result = service.dispatch_job()
    return DispatchJobResultPresenter.present_dispatch_job(result)