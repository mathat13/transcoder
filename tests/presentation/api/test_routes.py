from uuid import uuid4

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory
from tests.factories.pydantic_factories.radarr_webhook_factory import RadarrWebhookCreateRequestFactory

from application import (
    VerificationStarted,
    VerifyErrorJobNotFound,
    DispatchJobNoJobAvailable,
    JobDispatched,
    JobCreated,
)

from presentation import ManualCreateRequest

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

def test_dispatch_job_success(client, fake_job_service: FakeJobService):
    
    # Setup
    job = JobFactory(status=JobStatus.processing)
    ## Set fake_job_service.dispatch_job return value 
    fake_job_service.dispatch_job_fn=lambda: JobDispatched(job=job)

    # Execution
    response = client.post(f"/jobs/dispatch")

    # Verification
    assert response.status_code == 200
    assert response.json() == {
    "result": "job_dispatched",
    "job_id": str(job.id),
    "source_file": str(job.source_file.path),
    "output_file": str(job.transcode_output_file.path),
    }

def test_dispatch_job_no_job_available(client, fake_job_service: FakeJobService):

    # Setup
    ## Set fake_job_service.dispatch_job return value 
    fake_job_service.dispatch_job_fn=lambda: DispatchJobNoJobAvailable()

    # Execution
    response = client.post(f"/jobs/dispatch")

    # Verification
    assert response.status_code == 200
    assert response.json() == {
    "result": "no_job_available",
    "job_id": None,
    "source_file": None,
    "output_file": None,
    }

def test_create_job_success_with_manual_request(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    ## Set fake_job_service.dispatch_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreated(job=job)
    request = ManualCreateRequest(source_file=source_file)

    # Execution
    response = client.post(url=f"/jobs/create/manual", json=request.model_dump())

    # Verification
    assert response.status_code == 200
    assert response.json() == {
    "job_id": str(job.id),
    "status": job.status.value,
    "source_file": str(job.source_file.path),
    }

def test_create_job_success_with_radarr_webhook_request(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id
    ## Set fake_job_service.dispatch_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreated(job=job)
    request = RadarrWebhookCreateRequestFactory(movie__id=media_id, movieFile__sourceFile=source_file)

    # Execution
    response = client.post(url=f"/jobs/create/webhook/radarr", json=request.model_dump())

    # Verification
    assert response.status_code == 200
    assert response.json() == {
    "job_id": str(job.id),
    "status": job.status.value,
    "source_file": str(job.source_file.path),
    }


def test_create_job_success_with_radarr_webhook_request_with_extra_attributes(client,
                                                                              fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id
    ## Set fake_job_service.dispatch_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreated(job=job)
    request = RadarrWebhookCreateRequestFactory(movie__id=media_id,
                                                movieFile__sourceFile=source_file,
                                                movie__name='kiran',
                                                movieFile__name='kiran',
                                                name='kiran'
                                                )
    
    # Execution
    response = client.post(url=f"/jobs/create/webhook/radarr", json=request.model_dump())

    # Verification
    assert response.status_code == 200
    assert response.json() == {
    "job_id": str(job.id),
    "status": job.status.value,
    "source_file": str(job.source_file.path),
    }