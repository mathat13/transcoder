from uuid import UUID

from typing import Protocol, Optional
from domain import Job

class JobRepository(Protocol):

    def save(self, job: Job) -> None:
        ...

    def get(self, job_id: UUID) -> Optional[Job]:
        ...