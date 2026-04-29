import pytest
from uuid import uuid4
from fastapi import HTTPException

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import (
    VerifyJobResultPresenter,
    CreateJobResultPresenter,
    DispatchJobResultPresenter,
    VerifyJobResponse,
    DispatchJobResponse,
    CreateJobResponse,
    ErrorResponse,
    )

from application.result_types.jobservice_result_types import JobCreated
from application import (
    VerificationStarted,
    VerifyErrorJobNotFound,
    DispatchJobNoJobAvailable,
    JobDispatched,
)

def test_VerifyJobResultPresenter_with_VerificationStarted():
    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value 
    result = VerificationStarted(
            job=job,
        )
    
    # Exeution
    response = VerifyJobResultPresenter.present_verify_job(result=result)

    # Validation
    assert isinstance(response, VerifyJobResponse)
    assert response.model_dump() == {
        "id": str(job.id),
        "status": job.status.value,
    }

def test_VerifyJobResultPresenter_with_VerifyErrorJobNotFound():
    # Setup
    job_id = uuid4()
    result = VerifyErrorJobNotFound(
            job_id=job_id
            )
    
    # Exeution
    with pytest.raises(HTTPException) as exc:
        VerifyJobResultPresenter.present_verify_job(result=result)

    # Validation
    err = exc.value
    assert err.status_code == 404
    assert err.detail["error"] == "job_not_found"
    assert err.detail["job_id"] == str(job_id)

def test_CreateJobResultPresenter_with_JobCreated():
    # Setup
    job = JobFactory(status=JobStatus.pending)
    result = JobCreated(
            job=job
            )
    
    # Exeution
    response = CreateJobResultPresenter.present_create_job(result=result)

    # Validation
    assert isinstance(response, CreateJobResponse)
    assert response.model_dump() == {
        "job_id": str(job.id),
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
        "job_id": str(job.id),
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