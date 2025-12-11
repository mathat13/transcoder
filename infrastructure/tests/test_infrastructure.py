import pytest
from sqlalchemy import func

from domain import Job, JobStatus, FileInfo
from infrastructure import JobModel, JobRepository

def test_can_create_job(db_session):
    job = JobModel(
        job_type="episode",
        source_path="/input.mp4",
        status=JobStatus.pending.value,
    )

    db_session.add(job)
    db_session.commit()

    assert job.id is not None

def test_get_next_id(db_session):

    def get_next_id(db_session):
        last_id = db_session.query(func.max(JobModel.id)).scalar()
        return (last_id or 0) + 1
    
    assert get_next_id(db_session) == 1

    job = JobModel(
        job_type="episode",
        source_path="/input.mp4",
        status=JobStatus.pending.value,
    )

    db_session.add(job)
    db_session.commit()

    assert get_next_id(db_session) == 2

    job2 = JobModel(
        id=10,
        job_type="episode",
        source_path="/video2.mp4",
        status=JobStatus.pending.value
    )
    db_session.add(job2)
    db_session.commit()

    assert get_next_id(db_session) == 11

def test_job_repository_get_next_id(db_session, job_repository):
    assert job_repository.get_next_id() == 1

    job = JobModel(
        job_type="episode",
        source_path="/input.mp4",
        status=JobStatus.pending.value,
    )

    db_session.add(job)
    db_session.commit()

    assert job_repository.get_next_id() == 2

    job2 = JobModel(
        id=10,
        job_type="episode",
        source_path="/video2.mp4",
        status=JobStatus.pending.value
    )
    
    db_session.add(job2)
    db_session.commit()
    assert job_repository.get_next_id() == 11
