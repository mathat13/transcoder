from pydantic import BaseModel

from domain import Job

# DTOs

class CreateJobResponse(BaseModel):
    job_id: str
    status: str
    source_file: str

    @classmethod
    def from_job(cls, job: Job) -> "CreateJobResponse":
        return cls(
            job_id=str(job.id),
            status=job.status.value,
            source_file=str(job.source_file.path)
        )