from pydantic import BaseModel

from domain import Job

class VerifyJobResponse(BaseModel):
    id: str
    status: str

    @classmethod
    def from_job(cls, job: Job) -> "VerifyJobResponse":
        return cls(
            id=str(job.id),
            status=job.status.value,
        )
    
class ErrorResponse(BaseModel):
    error: str
    message: str | None = None
    job_id: str | None = None
    details: dict | None = None