from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
from uuid import uuid4, UUID

from domain.services.JobStateMachine import JOB_STATE_MACHINE
from domain.services.DomainEventFactory import DOMAIN_EVENT_FACTORY
from domain.value_objects.JobStatus import JobStatus
from domain.value_objects.ExternalMediaIDs import ExternalMediaIDs
from domain.value_objects.FileInfo import FileInfo

@dataclass
class Job:

    # Non-Default
    id: UUID
    source_file: FileInfo
    transcode_file: FileInfo
    external_media_ids: ExternalMediaIDs
    
    # Default
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

        event = DOMAIN_EVENT_FACTORY.create(self, old, new_status)
        self._emit(event)
    
    @classmethod
    def create(cls, source_file: FileInfo, media_ids: ExternalMediaIDs) -> "Job":
        """Factory for creating a valid Job aggregate."""
        transcode_file = source_file.transcode_file

        job = cls(
            id=uuid4(),
            source_file=source_file,
            transcode_file=transcode_file,
            external_media_ids=media_ids,
            status=JobStatus.pending,
        )
        
         # Emit the domain event *on the newly created instance*
        event = DOMAIN_EVENT_FACTORY.create(job, "created", job.status)
        job._emit(event)

        return job