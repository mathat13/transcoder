import pytest

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory
from tests.factories.pydantic_factories.radarr_webhook_factory import RadarrWebhookCreateJobRequestFactory

from application import (
    DispatchJobNoJobAvailable,
    JobDispatched,
    JobCreatedResult,
    CreateJobCommand,
)

from presentation import ManualCreateRequest

from domain import (
    JobStatus,
    OperationContext,
)

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
    assert json["id"] == str(job.id)
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
    assert json["id"] == None
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
    assert json["id"] == str(job.id)
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
    assert json["id"] == str(job.id)
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
    assert json["id"] == str(job.id)
    assert json["status"] == job.status.value
    assert json["source_file"] == str(job.source_file.path)