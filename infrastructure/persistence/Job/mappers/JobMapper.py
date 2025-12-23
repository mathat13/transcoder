from uuid import UUID

from domain import (
    Job,
    FileInfo,
    JobStatus
)

from infrastructure.persistence.Job.models.JobModel import JobModel

class JobMapper:

    @staticmethod
    def to_JobModel(job: Job) -> JobModel:
        return JobModel(
            id = str(job.id),
            job_type = job.job_type,
            source_path = job.source_file.path,
            transcode_path = job.transcode_file.path,
            status = job.status.value,
            # datetime object conversion handled by sqlalchemy
            created_at = job.created_at,
            updated_at  = job.updated_at
        )
    
    @staticmethod
    def to_Job(job_model: JobModel) -> Job:
        return Job(
            id = UUID(job_model.id),
            job_type = job_model.job_type,
            source_file = FileInfo(job_model.source_path),
            transcode_file = FileInfo(job_model.transcode_path),
            status = JobStatus(job_model.status),
            created_at = job_model.created_at,
            updated_at  = job_model.updated_at
        )
            
    


