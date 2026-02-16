from uuid import UUID
from typing import Protocol

from domain import Job

class JobPersistenceCapable(Protocol):
    def get_job_by_id(self, job_id: UUID) -> Job | None:
        ...
    
    def save(self, job: Job) -> None:
        ...

    def get_next_pending_job(self) -> Job | None:
        ...