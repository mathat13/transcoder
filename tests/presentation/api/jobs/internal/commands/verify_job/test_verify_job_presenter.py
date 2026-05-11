import pytest

from uuid import uuid4

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import (
    VerifyJobPresenter,
    VerifyJobResponse,
    VerifyJobErrorResponse,
    APIError,
    )

from application import (
    VerificationStarted,
    VerifyJobNotFound,
)

def test_VerifyJobPresenter_with_VerificationStarted():
    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value 
    result = VerificationStarted(
            job=job,
        )
    
    # Exeution
    response = VerifyJobPresenter.present(result=result)

    # Validation
    assert isinstance(response, VerifyJobResponse)
    assert response.model_dump() == {
        "result": "verification_started",
        "data": {
            "id": str(job.id),
            "status": job.status.value,
        },
        "meta": None,
    }

def test_VerifyJobPresenter_with_VerifyJobNotFound():
    # Setup
    id = uuid4()
    result = VerifyJobNotFound(
            id=id
            )
    
    # Exeution
    with pytest.raises(APIError) as exc:
        VerifyJobPresenter.present(result=result)

    # Validation
    err = exc.value
    assert err.status_code == 404

    response = err.response
    # Verify model as needs to be dumped to dict to be transported in exception
    assert isinstance(response, VerifyJobErrorResponse)
    assert response.model_dump() == {
        "error": "job_not_found",
        "data": {
            "id": str(id),
        },
        "meta": None,
    }