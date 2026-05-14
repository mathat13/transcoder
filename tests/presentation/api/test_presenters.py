import pytest

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import (
    CreateJobResultPresenter,
    CreateJobResponse,
    )

from application import JobCreatedResult

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