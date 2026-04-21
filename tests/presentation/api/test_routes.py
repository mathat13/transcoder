from uuid import uuid4

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from application import (
    VerificationStarted,
    VerifyErrorJobNotFound,
)

from domain import JobStatus

def test_verify_job_success(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value 
    fake_job_service.verify_job_fn=lambda job_id: VerificationStarted(
            job=job,
        )

    # Execution
    response = client.post(f"/jobs/{job.id}/verify")

    # Verification
    assert response.status_code == 200
    assert response.json() == {
    "id": str(job.id),
    "status": job.status.value
    }

def test_verify_job_job_not_found_error(client, fake_job_service: FakeJobService):

    # Setup
    job_id = uuid4()
    # Set fake_job_service.verify_job return value 
    fake_job_service.verify_job_fn=lambda job_id: VerifyErrorJobNotFound(
            job_id=job_id
            )

    # Execution
    response = client.post(f"/jobs/{job_id}/verify")

    # Verification
    assert response.status_code == 404
    assert response.json()["detail"] == {
    "error": "job_not_found",
    "message": None,
    "job_id": str(job_id),
    "details": None
    }

def test_verify_job_invalid_uuid(client):
    response = client.post("/jobs/not-a-uuid/verify")
    assert response.status_code == 422