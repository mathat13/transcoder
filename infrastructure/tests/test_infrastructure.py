import pytest
from uuid import UUID

from domain import Job, JobStatus, JobFactory, FileInfo
from infrastructure import JobModel, JobMapper, JobModelFactory

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
    converted_job = JobMapper.to_JobModel(job)

    db_session.add(converted_job)
    db_session.commit()
    db_session.refresh(converted_job)

    retrieved_job = job_repository._get_job_by_id(converted_job.id)

    assert retrieved_job.id == job.id

def test_JobModelFactory():
    pass

def test_JobRepository_get_next_pending_job(db_session, job_repository):
    job_models = JobModelFactory.build_batch(10, status="pending")

    assert len(job_models) == 10

    next_job_with_repo = job_repository.get_next_pending_job()
    next_job_direct = (
            db_session.query(JobModel)
            .filter(JobModel.status == "pending")
            .order_by(JobModel.created_at.asc())
            .first()
        )

    assert next_job_with_repo == next_job_direct






