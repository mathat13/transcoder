import pytest

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import (
    GetJobByIDResultPresenter,
    GetJobByIDResponse,
    )

from application import (
    GetJobByIDNotFound,
    GetJobByIDFound,
)

def test_GetJobByIDResultPresenter_with_GetJobByIDJobFound():
    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value
    result = GetJobByIDFound(job=job)
    
    # Exeution
    response = GetJobByIDResultPresenter.present(result=result)

    # Validation
    assert isinstance(response, GetJobByIDResponse)
    assert response.model_dump() == {
        "result": "job_found",
        "data": {
            "id": str(job.id),
            "source_file": str(job.source_file.path),
            "transcode_output_file": str(job.transcode_output_file.path),
            "delivery_file": str(job.delivery_file.path),
            "status": job.status.value
        },
        "meta": None,
    }

def test_GetJobByIDResultPresenter_with_GetJobByIDNotFound():
    # Setup
    result = GetJobByIDNotFound()
    
    # Exeution
    response = GetJobByIDResultPresenter.present(result=result)

    # Validation
    assert isinstance(response, GetJobByIDResponse)
    assert response.model_dump() == {
        "result": "job_not_found",
        "data": None,
        "meta": None,
    }