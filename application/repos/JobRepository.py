from typing import Protocol, Optional
from domain import Job

class JobRepository(Protocol):
    def next_id(self) -> int:
        ...

    def save(self, job: Job) -> None:
        ...

    def get(self, job_id: int) -> Optional[Job]:
        ...