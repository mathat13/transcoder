from domain import (
    JobStatus,
    Job,
    FileInfo
)

from tests import (
    JobFactory,
    FakeJobRepository,
    FakeFileSystem
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




