from domain import (
    JobStatus,
    Job
)

from tests import (
    JobFactory,
    FakeJobRepository
)


def test_FakeJobRepository_get_next_pending_job():
    repo = FakeJobRepository()

    job1 = JobFactory(status=JobStatus.processing)
    job2 = JobFactory()

    repo.save(job1)
    repo.save(job2)

    retrieved_job = repo.get_next_pending_job()

    assert isinstance(retrieved_job, Job)
    assert retrieved_job.status == JobStatus.pending


