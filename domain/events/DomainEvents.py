from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.value_objects.FileInfo import FileInfo
from domain.value_objects.ExternalMediaIDs import ExternalMediaIDs
from domain.value_objects.JobStatus import JobStatus
from domain.events.Base import Event

@dataclass(kw_only=True)
class DomainEvent(Event):
    pass

@dataclass(kw_only=True)
class JobStatusChanged(DomainEvent):
    job_id: UUID
    old_status: JobStatus
    new_status: JobStatus

@dataclass(kw_only=True)
class JobCreated(DomainEvent):
    job_id: UUID
    source_file: FileInfo

@dataclass(kw_only=True)
class JobMovedToProcessing(DomainEvent):
    job_id: UUID

@dataclass(kw_only=True)
class JobMovedToVerifying(DomainEvent):
    job_id: UUID
    transcode_output_file: FileInfo

@dataclass(kw_only=True)
class JobCompleted(DomainEvent):
    job_id: UUID
    source_file: FileInfo
    transcode_output_file: FileInfo
    delivery_file: FileInfo
    media_ids: Optional[ExternalMediaIDs]

@dataclass(kw_only=True)
class JobFailed(DomainEvent):
    job_id: UUID
    reason: Optional[str] = None