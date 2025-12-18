from dataclasses import dataclass
from typing import Optional

from domain.value_objects.FileInfo import FileInfo
from domain.events.Base import Event

@dataclass(kw_only=True)
class DomainEvent(Event):
    pass

@dataclass(kw_only=True)
class JobStatusChanged(DomainEvent):
    job_id: int
    old_status: FileInfo
    new_status: FileInfo

@dataclass(kw_only=True)
class JobCreated(DomainEvent):
    job_id: int
    source_path: FileInfo

@dataclass(kw_only=True)
class JobMovedToProcessing(DomainEvent):
    job_id: int

@dataclass(kw_only=True)
class JobMovedToVerifying(DomainEvent):
    job_id: int
    output_path: FileInfo

@dataclass(kw_only=True)
class JobCompleted(DomainEvent):
    job_id: int

@dataclass(kw_only=True)
class JobFailed(DomainEvent):
    job_id: int
    reason: Optional[str] = None