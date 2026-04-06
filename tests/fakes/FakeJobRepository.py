from uuid import UUID

from typing import Dict

from domain import (
    Job,
    JobStatus
)

class FakeJobRepository:
    def __init__(self):
        self._store: Dict[UUID, Job] = {}

    def get_job_by_id(self, job_id: UUID) -> Job | None:
        return self._store.get(job_id)

    def save(self, job: Job) -> None:
        self._store[job.id] = job
    
    def delete(self, job_id: UUID) -> None:
        
        
        if not self._store.get(job_id):
        # Idempotent: nothing to delete
            return

        del self._store[job_id]
        
    def get_next_pending_job(self) -> Job | None:
        return next((obj for obj in self._store.values() if obj.status == JobStatus.pending), None)
    

