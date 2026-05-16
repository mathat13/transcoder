import pytest

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from application import (
    JobCreatedResult,
    CreateJobCommand,
)

from tests.factories.pydantic_factories.radarr_webhook_factory import CreateJobRequestFactory

from domain import OperationContext

def test_create_job_success_with_radarr_webhook_request(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id
    ## Set fake_job_service.create_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreatedResult(job=job)
    request = CreateJobRequestFactory(movie__id=media_id,
                                                   movieFile__sourceFile=source_file)

    # Execution
    response = client.post(url=f"/jobs/create/webhook/radarr", json=request.model_dump())

    # Verification
    assert isinstance(fake_job_service.last_ctx, OperationContext)
    assert isinstance(fake_job_service.last_cmd, CreateJobCommand)
    assert fake_job_service.create_job_calls == 1

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "job_created"
    assert json["data"] != {}
    assert json["meta"] == {}

def test_create_job_ingress_ignore_with_radarr_webhook_request(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id

    request = CreateJobRequestFactory(movie__id=media_id,
                                      movieFile__sourceFile=source_file,
                                      eventType="not_a_download"
                                      )

    # Execution
    response = client.post(url=f"/jobs/create/webhook/radarr", json=request.model_dump())

    assert response.status_code == 200

def test_create_job_success_with_radarr_webhook_request_with_extra_attributes(client,
                                                                              fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    media_id = job.external_media_ids.radarr_movie_id
    ## Set fake_job_service.dispatch_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreatedResult(job=job)
    request = CreateJobRequestFactory(movie__id=media_id,
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
    assert json["result"] == "job_created"
    assert json["data"] != {}
    assert json["meta"] == {}