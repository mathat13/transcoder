import pytest

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from application import (
    NoJobAvailable,
    JobDispatched,
)

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
    assert json["data"] is not None
    assert json["meta"] is None

def test_dispatch_job_no_job_available(client, fake_job_service: FakeJobService):

    # Setup
    ## Set fake_job_service.dispatch_job return value 
    fake_job_service.dispatch_job_fn=lambda ctx: NoJobAvailable()

    # Execution
    response = client.post(f"/jobs/dispatch")

    # Verification
    assert fake_job_service.dispatch_job_calls == 1
    assert isinstance(fake_job_service.last_ctx, OperationContext)

    assert response.status_code == 200
    json = response.json()
    assert json["result"] == "no_job_available"
    assert json["data"] == {}
    assert json["meta"] is None