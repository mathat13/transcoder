from uuid import UUID

from domain import (
    Job,
    JobStatus
)

class FakeJobRepository:
    def __init__(self):
        self._store = {}

    def _get_job_by_id(self, job_id: UUID) -> Job | None:
        return self._store.get(job_id)

    def save(self, job: Job) -> None:
        self._store[job.id] = job
        
    def get_next_pending_job(self) -> Job | None:
        return next((obj for obj in self._store.values() if obj.status == JobStatus.pending), None)
    

