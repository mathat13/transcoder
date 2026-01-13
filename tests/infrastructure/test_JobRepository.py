import pytest
from datetime import datetime
from uuid import UUID

from infrastructure import (
    JobMapper,
    JobModel
)

from domain import (
    Job,
    FileInfo,
    JobStatus,
    ExternalMediaIDs,
)
from tests import (
    JobFactory
)

def test_JobMapper():
    job = JobFactory()
    job_record = JobMapper.to_JobModel(job)

    assert isinstance(job_record, JobModel)
    assert isinstance(job_record.id, str)
    assert isinstance(job_record.radarr_id, int)
    assert isinstance(job_record.source_path, str)
    assert isinstance(job_record.transcode_path, str)
    assert isinstance(job_record.status, str)
    assert isinstance(job_record.created_at, datetime)
    assert isinstance(job_record.updated_at, datetime)
    assert job_record.source_path == job.source_file.path
    assert job_record.transcode_path == job.transcode_file.path

    converted_job = JobMapper.to_Job(job_record)

    assert isinstance(converted_job, Job)
    assert isinstance(converted_job.id, UUID)
    assert isinstance(converted_job.external_media_ids, ExternalMediaIDs)
    assert isinstance(converted_job.external_media_ids.radarr_movie_id, int)
    assert isinstance(converted_job.source_file, FileInfo)
    assert isinstance(converted_job.transcode_file, FileInfo)
    assert isinstance(converted_job.status, JobStatus)
    assert isinstance(converted_job.created_at, datetime)
    assert isinstance(converted_job.updated_at, datetime)
    assert job_record.source_path == converted_job.source_file.path
    assert job_record.transcode_path == converted_job.transcode_file.path

def test_JobRepository_save(db_session, job_repository):
    job = JobFactory()

    job_repository.save(job)

    # Manually retrieve record from db
    retrieved_job = db_session.query(JobModel).filter(JobModel.id == str(job.id)).first()

    # Retrieved job doesn't use JobMapper and so returns a JobModel
    assert retrieved_job.id == str(job.id)

def test_JobRepository_get_job_by_id(db_session, job_repository):
    job = JobFactory()
    job_model = JobMapper.to_JobModel(job)

    db_session.add(job_model)
    db_session.commit()
    db_session.refresh(job_model)

    retrieved_job = job_repository._get_job_by_id(job.id)

    assert isinstance(retrieved_job, Job)
    assert str(retrieved_job.id) == job_model.id

def test_JobRepository_get_next_pending_job(db_session, job_repository, job_model_factory):
    job_model_factory.create_batch(10, status="pending")

    next_job_with_repo = job_repository.get_next_pending_job()
    next_job_direct = (
            db_session.query(JobModel)
            .filter(JobModel.status == "pending")
            .order_by(JobModel.created_at.asc())
            .first()
        )
    
    assert isinstance(next_job_with_repo, Job)
    assert isinstance(next_job_direct, JobModel)
    assert str(next_job_with_repo.id) == next_job_direct.id

def test_JobRepository_get_next_pending_job_no_job_model(db_session, job_repository):
    # Grabbing from empty db
    next_job_with_repo = job_repository.get_next_pending_job()

    next_job_direct = (
            db_session.query(JobModel)
            .filter(JobModel.status == "pending")
            .order_by(JobModel.created_at.asc())
            .first()
        )
    
    assert next_job_direct is None
    assert next_job_with_repo is None