from domain import Job, FileInfo, JobStatus
from infrastructure.persistence.models.JobModel import JobModel

class JobMapper:

    @staticmethod
    def to_JobModel(job: Job) -> JobModel:
        return JobModel(
            id = job.id,
            job_type = job.job_type,
            source_path = job.source_path.path,
            output_path = job.output_path.path,
            status = job.status.value,
            created_at = job.created_at,
            updated_at  = job.updated_at
        )
    
    @staticmethod
    def to_Job(job_model: JobModel) -> Job:
        return JobModel(
            id = job_model.id,
            job_type = job_model.job_type,
            source_path = FileInfo(job_model.source_path),
            output_path = FileInfo(job_model.output_path),
            status = JobStatus(job_model.status),
            created_at = job_model.created_at,
            updated_at  = job_model.updated_at
        )
            
    


