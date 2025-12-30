from domain import (
    JobStatus,
    Job,
    FileInfo
)

from tests import (
    JobFactory,
    FakeJobRepository,
    FakeFileSystem,
    FakeHTTPClient
)

from infrastructure import (
    HTTPResponse,
    
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

def test_FakeFileSystem_exists_returns_true_with_existing_file():
    fs = FakeFileSystem()

    file = FileInfo("/fake/file.mp4")

    fs.add(file)

    result = fs.exists(file)

    assert result is True

def test_FakeFileSystem_exists_returns_false_with_non_existing_file():
    fs = FakeFileSystem()

    file = FileInfo("/fake/file.mp4")

    # Don't add to fake filesystem

    result = fs.exists(file)

    assert result is False

def test_FakeHTTPClient_get_method():

    url = "https://example.com/api/resource"
    headers = {"Authorization": "Bearer token"}
    query_params = {"id": 3}
    fake_response = HTTPResponse(
        ok=True,
        status_code=200,
        headers=headers,
        url=url,
        data={}
    )
    client = FakeHTTPClient(response=fake_response)

    response = client.get(url, headers, query_params)

    assert response == fake_response
    assert response.ok is True
    assert response.status_code == 200
    assert response.headers == headers
    assert response.url == url
    assert response is fake_response
    




