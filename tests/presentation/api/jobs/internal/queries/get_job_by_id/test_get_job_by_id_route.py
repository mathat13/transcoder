from uuid import  UUID

from tests.fakes.FakeJobService import FakeJobService
from tests.factories.JobFactory import JobFactory

from application import (
    GetJobByIDFound,
    GetJobByIDNotFound,
)

from domain import (
    OperationContext,
)

def test_get_job_by_id_success(client, fake_job_service: FakeJobService):

    # Setup
    job = JobFactory()
    ## Set fake_job_service.create_job return value
    fake_job_service.get_job_by_id_fn=lambda id, ctx: GetJobByIDFound(job=job)

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
    fake_job_service.get_job_by_id_fn=lambda id, ctx: GetJobByIDNotFound()

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