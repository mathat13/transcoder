from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4, UUID

from domain.services.JobStateMachine import JOB_STATE_MACHINE
from domain.services.DomainEventFactory import DOMAIN_EVENT_FACTORY
from domain.value_objects.JobStatus import JobStatus
from domain.value_objects.ExternalMediaIDs import ExternalMediaIDs
from domain.value_objects.FileInfo import FileInfo
from domain.events.DomainEvents import DomainEvent

@dataclass
class Job:

    # Non-Default
    id: UUID
    source_file: FileInfo
    transcode_output_file: FileInfo
    delivery_file: FileInfo
    external_media_ids: Optional[ExternalMediaIDs]
    
    # Default
    status: JobStatus = JobStatus.pending
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    events: List[DomainEvent] = field(default_factory=list, init=False)

    # ---------------------------
    # INTERNAL HELPERS
    # ---------------------------

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _emit(self, event: DomainEvent):
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
    def _create_for_test(
        cls,
        *,
        id: UUID,
        source_file: FileInfo,
        transcode_output_file: FileInfo,
        media_ids: Optional[ExternalMediaIDs],
        status: JobStatus,
    ) -> "Job":
        return cls(
            id=id,
            source_file=source_file,
            transcode_output_file=transcode_output_file,
            delivery_file=FileInfo.from_parent_and_name(source_file.parent, transcode_output_file.name),
            external_media_ids=media_ids,
            status=status,
        )
    
    @classmethod
    def create(cls, source_file: FileInfo, transcode_output_file: FileInfo, media_ids: Optional[ExternalMediaIDs]) -> "Job":
        """Factory for creating a valid Job aggregate."""

        job = cls(
            id=uuid4(),
            source_file=source_file,
            transcode_output_file=transcode_output_file,
            delivery_file=FileInfo.from_parent_and_name(source_file.parent, transcode_output_file.name),
            external_media_ids=media_ids or None,
            status=JobStatus.pending,
        )
        
         # Emit the domain event *on the newly created instance*
        event = DOMAIN_EVENT_FACTORY.create(job, "created", job.status)
        job._emit(event)

        return job
    
    @classmethod
    def rehydrate(cls,
                  job_id: UUID,
                  source_file: FileInfo,
                  transcode_output_file: FileInfo,
                  media_ids: Optional[ExternalMediaIDs],
                  status: JobStatus,
                  ) -> "Job":
        """Factory for rehydrating a valid Job aggregate from persistence."""

        return cls(
            id=job_id,
            source_file=source_file,
            transcode_output_file=transcode_output_file,
            delivery_file=FileInfo.from_parent_and_name(source_file.parent, transcode_output_file.name),
            external_media_ids=media_ids or None,
            status=status,
        )
    
    # ---------------------------
    # Event helpers
    # ---------------------------

    def pull_events(self):
        events = self.events[:]
        self.events.clear()
        return events