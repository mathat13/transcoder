from domain import (
    JobStatus,
    Job,
    FileInfo,
    ExternalMediaIDs,
)

from tests import (
    JobFactory,
    FakeJobRepository,
    FakeHTTPClient
)

from infrastructure import (
    HTTPResponse,
    HTTPRequest
)


def test_FakeJobRepository_get_next_pending_job_gets_next_pending_job():
    repo = FakeJobRepository()

    job1 = JobFactory(status=JobStatus.processing)
    job2 = JobFactory()

    repo.save(job1)
    repo.save(job2)

    retrieved_job = repo.get_next_pending_job()

    assert isinstance(retrieved_job, Job)
    assert retrieved_job.status == JobStatus.pending

def test_FakeHTTPClient_send_method():
    url = "https://example.com/api/resource"
    headers = {"Authorization": "Bearer token"}
    query_params = {"id": 3}

    request = HTTPRequest(
        url=url,
        headers=headers,
        query_params=query_params
    )

    fake_response = HTTPResponse(
        ok=True,
        status_code=200,
        headers=headers,
        url=url,
        json_data={"message": "hello"}
    )
    client = FakeHTTPClient(response=fake_response)

    response = client._send(request)

    assert response is fake_response

def test_FakeJobRepository_saves_job_correctly():
    repo = FakeJobRepository()

    job = Job.create(
        source_file=FileInfo("/input.mp4"),
        media_ids=ExternalMediaIDs(1)
    )

    # Save job
    repo.save(job)

    # Load saved job
    saved = repo._get_job_by_id(job.id)
    assert saved.id == job.id
    assert saved.source_file == job.source_file
    assert saved.status == job.status
    assert saved.external_media_ids == job.external_media_ids
    




