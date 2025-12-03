from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from domain.events.JobEvents import JobStatusChanged, JobCreated
from domain.services.JobStateMachine import JOB_STATE_MACHINE
from domain.value_objects.JobStatus import JobStatus

@dataclass
class Job:
    id: int | None
    job_type: str
    source_path: str
    output_path: str | None
    status: JobStatus = JobStatus.pending

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    events: List = field(default_factory=list, init=False)

    # ---------------------------
    # INTERNAL HELPERS
    # ---------------------------

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _emit(self, event):
        self.events.append(event)

    # ---------------------------
    # DOMAIN OPERATIONS
    # ---------------------------

    def transition_to(self, new_status: JobStatus) -> None:
        """Perform a legal state transition according to the state machine."""
        allowed = JOB_STATE_MACHINE.get(self.status, [])
        if new_status not in allowed:
            raise ValueError(f"Invalid transition {self.status} → {new_status}")

        old = self.status
        self.status = new_status
        self.updated_at = self._now()

        self._emit(JobStatusChanged(
            job_id=self.id,
            old_status=old.value,
            new_status=new_status.value,
        ))
    
    @classmethod
    def create(cls, job_id: int, job_type: str, source_path: str) -> Job:
        """Factory for creating a valid Job aggregate."""
        job = cls(
            id=job_id,
            job_type=job_type,
            source_path=source_path,
            output_path=None,
            status=JobStatus.pending,
        )
        
         # Emit the domain event *on the newly created instance*
        job._emit(JobCreated(
            job_id=job.id,
            job_status=job.status.value,
            source_path=job.source_path,
        ))

        return job