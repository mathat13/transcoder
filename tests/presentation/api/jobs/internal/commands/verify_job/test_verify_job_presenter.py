import pytest

from uuid import uuid4

from tests.factories.JobFactory import JobFactory

from domain import JobStatus

from presentation import (
    VerifyJobPresenter,
    ApplicationFailure,
    )

from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.success.response import VerificationStartedResponse
from presentation.api.use_cases.jobs.internal.commands.verify_job.egress.responses.failure.response import JobNotFoundResponse
from application.services.jobs.commands.verify_job.results import (
    VerificationStarted,
    JobNotFound,
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
    assert isinstance(response, VerificationStartedResponse)
    assert response.model_dump() == {
        "result": "verification_started",
        "data": {
            "id": str(job.id),
            "status": job.status.value,
        },
        "meta": None,
    }

def test_VerifyJobPresenter_with_JobNotFound():
    # Setup
    id = uuid4()
    result = JobNotFound(
            id=id
            )
    
    # Exeution
    with pytest.raises(ApplicationFailure) as exc:
        VerifyJobPresenter.present(result=result)

    # Validation
    err = exc.value
    assert err.status_code == 404

    response = err.response
    assert isinstance(response, JobNotFoundResponse)
    assert response.model_dump() == {
        "error": "job_not_found",
        "data": {
            "id": str(id),
        },
        "meta": None,
    }