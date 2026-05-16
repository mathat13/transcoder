import pytest

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from application import (
    JobCreatedResult,
    CreateJobCommand,
)

from presentation.api.use_cases.jobs.internal.commands.create_job.ingress.request import CreateJobRequest

from domain import OperationContext

def test_create_job_success(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    source_file = str(job.source_file.path)
    ## Set fake_job_service.create_job return value
    fake_job_service.create_job_fn=lambda cmd, ctx: JobCreatedResult(job=job)
    request = CreateJobRequest(source_file=source_file)

    # Execution
    response = client.post(url=f"/jobs/create", json=request.model_dump())

    # Verification
    assert fake_job_service.create_job_calls == 1
    assert isinstance(fake_job_service.last_cmd, CreateJobCommand)
    assert isinstance(fake_job_service.last_ctx, OperationContext)

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "job_created"
    assert json["data"] != {}
    assert json["meta"] == {}