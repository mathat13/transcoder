import pytest
from sqlalchemy import func
from uuid import UUID

from domain import Job, JobStatus, JobFactory, FileInfo
from infrastructure import JobModel, JobMapper

def test_can_create_job(db_session):
    job = JobModel(
        job_type="episode",
        source_path="/input.mp4",
        status=JobStatus.pending.value,
    )

    db_session.add(job)
    db_session.commit()

    assert job.id is not None

def test_JobMapper():
    job = JobFactory()
    job_record = JobMapper.to_JobModel(job)

    assert isinstance(job_record.id, str)
    assert isinstance(job_record.source_path, str)
    assert isinstance(job_record.output_path, str)
    assert isinstance(job_record.status, str)
    assert job_record.source_path == job.source_path.path
    assert job_record.output_path == job.output_path.path

    converted_job = JobMapper.to_Job(job_record)

    assert isinstance(converted_job.id, UUID)
    assert isinstance(converted_job.source_path, FileInfo)
    assert isinstance(converted_job.output_path, FileInfo)
    assert isinstance(converted_job.status, JobStatus)
    assert job_record.source_path == converted_job.source_path.path
    assert job_record.output_path == converted_job.output_path.path

def test_JobRepository_save(db_session, job_repository):
    job = JobFactory()
    str_job_id = str(job.id)
    job_repository.save(job)

    # Manually retrieve record from db
    retrieved_job = db_session.query(JobModel).filter(JobModel.id == str_job_id).first()

    assert retrieved_job.id == str_job_id

def test_JobRepository_get_job_by_id(db_session, job_repository):
    job = JobFactory()

    db_session.add(job)
    db_session.commit()

    retrieved_job = job_repository.get_job_by_id(job.id)

    assert retrieved_job.id == job.id





