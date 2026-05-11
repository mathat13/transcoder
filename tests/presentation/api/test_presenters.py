import pytest

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import (
    CreateJobResultPresenter,
    DispatchJobResultPresenter,
    DispatchJobResponse,
    CreateJobResponse,
    )

from application import (
    DispatchJobNoJobAvailable,
    JobDispatched,
    JobCreatedResult,
)

def test_CreateJobResultPresenter_with_JobCreatedResult():
    # Setup
    job = JobFactory(status=JobStatus.pending)
    result = JobCreatedResult(
            job=job
            )
    
    # Exeution
    response = CreateJobResultPresenter.present_create_job(result=result)

    # Validation
    assert isinstance(response, CreateJobResponse)
    assert response.model_dump() == {
        "id": str(job.id),
        "status": job.status.value,
        "source_file": str(job.source_file.path)
    }

def test_DispatchJobResultPresenter_with_JobDispatched():
    # Setup
    job = JobFactory(status=JobStatus.processing)
    result = JobDispatched(
            job=job
            )
    
    # Exeution
    response = DispatchJobResultPresenter.present_dispatch_job(result=result)

    # Validation
    assert isinstance(response, DispatchJobResponse)
    assert response.model_dump() == {
        "result": "job_dispatched",
        "id": str(job.id),
        "source_file": str(job.source_file.path),
        "output_file": str(job.transcode_output_file.path)
    }

def test_DispatchJobResultPresenter_with_DispatchJobNoJobAvailable():
    # Setup
    result = DispatchJobNoJobAvailable()
    
    # Exeution
    response = DispatchJobResultPresenter.present_dispatch_job(result=result)

    # Validation
    assert isinstance(response, DispatchJobResponse)
    assert response.result == "no_job_available"