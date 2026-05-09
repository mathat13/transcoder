from pydantic import BaseModel
from typing import Literal

from domain import Job

from typing import TypeVar

T = TypeVar("T")

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

class DispatchJobResponse(BaseModel):
    result: Literal["job_dispatched", "no_job_available"]
    job_id: str | None = None
    source_file: str | None = None
    output_file: str | None = None

    @classmethod
    def from_job(cls, job: Job) -> "DispatchJobResponse":
        return cls(
            result="job_dispatched",
            job_id=str(job.id),
            source_file=str(job.source_file.path),
            output_file=str(job.transcode_output_file.path),
        )
    
    @classmethod
    def no_job_available(cls) -> "DispatchJobResponse":
        return cls(result="no_job_available")