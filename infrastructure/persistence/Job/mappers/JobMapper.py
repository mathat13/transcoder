from uuid import UUID

from domain import (
    Job,
    FileInfo,
    JobStatus,
    ExternalMediaIDs,
)

from infrastructure.persistence.Job.models.JobModel import JobModel

class JobMapper:

    @staticmethod
    def to_JobModel(job: Job) -> JobModel:
        return JobModel(
            id = str(job.id),
            external_media_ids = job.external_media_ids,
            source_file = str(job.source_file.path),
            transcode_output_file = str(job.transcode_output_file.path),
            delivery_file = str(job.delivery_file.path),
            status = job.status.value,
            # datetime object conversion handled by sqlalchemy
            created_at = job.created_at,
            updated_at  = job.updated_at
        )
    
    # Update this method to call a reconstitute factory method in Job object
    @staticmethod
    def to_Job(job_model: JobModel) -> Job:
        return Job(
            id = UUID(job_model.id),
            external_media_ids=job_model.external_media_ids,
            source_file = FileInfo.from_path(job_model.source_file),
            transcode_output_file = FileInfo.from_path(job_model.transcode_output_file),
            delivery_file = FileInfo.from_path(job_model.delivery_file),
            status = JobStatus(job_model.status),
            created_at = job_model.created_at,
            updated_at  = job_model.updated_at
        )
            
    


