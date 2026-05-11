import pytest

from uuid import uuid4, UUID

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from application import (
    VerificationStarted,
    VerifyJobNotFound,
)

from domain import (
    JobStatus,
    OperationContext,
)

def test_verify_job_success(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value 
    fake_job_service.verify_job_fn=lambda id, ctx: VerificationStarted(
            job=job,
        )

    # Execution
    response = client.post(f"/jobs/{job.id}/verify")

    # Verification
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert isinstance(fake_job_service.last_cmd, UUID)
    assert fake_job_service.verify_job_calls == 1

    assert response.status_code == 200

    json = response.json()
    assert json["result"] == "verification_started"
    assert json["data"] is not None
    assert json["meta"] is None

def test_verify_job_job_not_found_error(client, fake_job_service: FakeJobService):

    # Setup
    id = uuid4()
    # Set fake_job_service.verify_job return value 
    fake_job_service.verify_job_fn=lambda id, ctx: VerifyJobNotFound(
            id=id
            )

    # Execution
    response = client.post(f"/jobs/{id}/verify")

    # Validation
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert isinstance(fake_job_service.last_cmd, UUID)
    assert fake_job_service.verify_job_calls == 1

    assert response.status_code == 404
    json = response.json()
    assert json["error"] == "job_not_found"
    assert json["data"] is not None
    assert json["meta"] is None

def test_verify_job_invalid_uuid(client):
    response = client.post("/jobs/not-a-uuid/verify")
    assert response.status_code == 422