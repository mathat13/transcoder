from uuid import uuid4, UUID

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory
from tests.factories.pydantic_factories.radarr_webhook_factory import RadarrWebhookCreateJobRequestFactory

from application import (
    VerificationStarted,
    VerifyErrorJobNotFound,
    DispatchJobNoJobAvailable,
    JobDispatched,
    JobCreatedResult,
    CreateJobCommand,
    GetJobByIDFound,
    GetJobByIDNotFound,
)
# Imported indiviually due to having the same name as an event in application layer (whoops)

from presentation import ManualCreateRequest

from domain import (
    JobStatus,
    OperationContext,
)

def test_verify_job_success(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory(status=JobStatus.verifying)
    # Set fake_job_service.verify_job return value 
    fake_job_service.verify_job_fn=lambda job_id, ctx: VerificationStarted(
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
    assert json["id"] == str(job.id)
    assert json["status"] == job.status.value

def test_verify_job_job_not_found_error(client, fake_job_service: FakeJobService):

    # Setup
    job_id = uuid4()
    # Set fake_job_service.verify_job return value 
    fake_job_service.verify_job_fn=lambda job_id, ctx: VerifyErrorJobNotFound(
            job_id=job_id
            )

    # Execution
    response = client.post(f"/jobs/{job_id}/verify")

    # Verification
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert fake_job_service.verify_job_calls == 1

    assert response.status_code == 404
    json = response.json()
    assert json["detail"]["error"] == "job_not_found"
    assert json["detail"]["job_id"] == str(job_id)

def test_verify_job_invalid_uuid(client):
    response = client.post("/jobs/not-a-uuid/verify")
    assert response.status_code == 422

def test_dispatch_job_success(client, fake_job_service: FakeJobService):
    
    # Setup
    job = JobFactory(status=JobStatus.processing)
    ## Set fake_job_service.dispatch_job return value 
    fake_job_service.dispatch_job_fn=lambda ctx: JobDispatched(job=job)

    # Execution
    response = client.post(f"/jobs/dispatch")

    # Verification
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert fake_job_service.dispatch_job_calls == 1

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "job_dispatched"
    assert json["job_id"] == str(job.id)
    assert json["source_file"] == str(job.source_file.path)
    assert json["output_file"] == str(job.transcode_output_file.path)

def test_dispatch_job_no_job_available(client, fake_job_service: FakeJobService):

    # Setup
    ## Set fake_job_service.dispatch_job return value 
    fake_job_service.dispatch_job_fn=lambda ctx: DispatchJobNoJobAvailable()

    # Execution
    response = client.post(f"/jobs/dispatch")

    # Verification
    assert fake_job_service.dispatch_job_calls == 1
    assert isinstance(fake_job_service.last_ctx, OperationContext)

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "no_job_available"
    assert json["job_id"] == None
    assert json["source_file"] == None
    assert json["output_file"] == None

def test_create_job_success_with_manual_request(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    ## Set fake_job_service.create_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreatedResult(job=job)
    request = ManualCreateRequest(source_file=source_file)

    # Execution
    response = client.post(url=f"/jobs/create/manual", json=request.model_dump())

    # Verification
    assert fake_job_service.create_job_calls == 1
    assert isinstance(fake_job_service.last_cmd, CreateJobCommand)
    assert isinstance(fake_job_service.last_ctx, OperationContext)

    assert response.status_code == 200
    json = response.json()
    assert json["job_id"] == str(job.id)
    assert json["status"] == job.status.value
    assert json["source_file"] == str(job.source_file.path)

def test_create_job_success_with_radarr_webhook_request(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id
    ## Set fake_job_service.create_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreatedResult(job=job)
    request = RadarrWebhookCreateJobRequestFactory(movie__id=media_id,
                                                   movieFile__sourceFile=source_file)

    # Execution
    response = client.post(url=f"/jobs/create/webhook/radarr", json=request.model_dump())

    # Verification
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert isinstance(fake_job_service.last_cmd, CreateJobCommand)
    assert fake_job_service.create_job_calls == 1

    assert response.status_code == 200
    json = response.json()
    assert json["job_id"] == str(job.id)
    assert json["status"] == job.status.value
    assert json["source_file"] == str(job.source_file.path)

def test_create_job_success_with_radarr_webhook_request_with_extra_attributes(client,
                                                                              fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id
    ## Set fake_job_service.dispatch_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreatedResult(job=job)
    request = RadarrWebhookCreateJobRequestFactory(movie__id=media_id,
                                                movieFile__sourceFile=source_file,
                                                # Extra ignored attributes
                                                movie__name='kiran',
                                                movieFile__name='kiran',
                                                name='kiran'
                                                )
    
    # Execution
    response = client.post(url=f"/jobs/create/webhook/radarr", json=request.model_dump())

    # Verification
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert isinstance(fake_job_service.last_cmd, CreateJobCommand)
    assert fake_job_service.create_job_calls == 1

    assert response.status_code == 200
    json = response.json()
    assert json["job_id"] == str(job.id)
    assert json["status"] == job.status.value
    assert json["source_file"] == str(job.source_file.path)

def test_get_job_by_id_success(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    ## Set fake_job_service.create_job return value
    fake_job_service.get_job_by_id_fn=lambda job_id, ctx: GetJobByIDFound(job=job)

    # Execution
    response = client.get(url=f"/jobs/{job.id}")

    # Verification
    assert fake_job_service.get_job_by_id_calls == 1
    assert isinstance(fake_job_service.last_cmd, UUID)
    assert isinstance(fake_job_service.last_ctx, OperationContext)

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "job_found"
    assert json["data"] is not None
    assert json["meta"] is None

def test_get_job_by_id_no_job_found(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    ## Set fake_job_service.get_job_by_id return value
    fake_job_service.get_job_by_id_fn=lambda job_id, ctx: GetJobByIDNotFound()

    # Execution
    response = client.get(url=f"/jobs/{job.id}")

    # Verification
    assert fake_job_service.get_job_by_id_calls == 1
    assert isinstance(fake_job_service.last_cmd, UUID)
    assert isinstance(fake_job_service.last_ctx, OperationContext)

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "job_not_found"
    assert json["data"] is None
    assert json["meta"] is None