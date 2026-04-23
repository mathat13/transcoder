from fastapi import APIRouter, Depends
from uuid import UUID

from presentation.api.presenters.create_job import CreateJobResultPresenter
from presentation.api.presenters.verify_job import VerifyJobResultPresenter
from presentation.api.presenters.dispatch_job import DispatchJobResultPresenter
from presentation.api.schemas.responses import (
    VerifyJobResponse,
    DispatchJobResponse,
    CreateJobResponse,
)
from presentation.api.schemas.requests import ManualCreateRequest



from presentation.api.dependencies import get_job_service

from application import (
    JobService,
    CreateJobCommand,
)

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

@router.post("/create/manual", response_model=CreateJobResponse)
def create_manual_job(
    request: ManualCreateRequest,
    service: JobService = Depends(get_job_service)
):
    cmd = CreateJobCommand.from_manual(
        source_file=request.source_file,
    )

    result = service.create_job(cmd=cmd, ctx=None)
    return CreateJobResultPresenter.present_create_job(result)

#@router.post("/create/webhook/radarr", response_model=CreateJobResponse)
#def create_job(
#    payload: str,
#    service: JobService = Depends(get_job_service)
#):
#    cmd = CreateJobCommand.from_radarr(
#        source_file=source_file,
#        media_id=
#    )
#    result = service.create_job(cmd=cmd)
#    return CreateJobResultPresenter.present_create_job(result)