from fastapi.testclient import TestClient
from fastapi import FastAPI
from uuid import uuid4

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from presentation import (
    router as jobs_router,
    get_job_service,
)

from application import VerificationStarted

from domain import JobStatus

def test_verify_job_success(client, fake_job_service: FakeJobService):

    job_id = uuid4()

    fake_job_service.verify_job_fn=lambda job_id: VerificationStarted(
            job=JobFactory(id=job_id, status=JobStatus.verifying)
        )

    response = client.post(f"/jobs/{job_id}/verify")

    assert response.status_code == 200
    assert response.json()["id"] == str(job_id)