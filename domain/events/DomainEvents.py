from dataclasses import dataclass
from typing import Optional

from domain.value_objects.FileInfo import FileInfo

@dataclass
class DomainEvent:
    pass

@dataclass
class JobStatusChanged(DomainEvent):
    job_id: int
    old_status: FileInfo
    new_status: FileInfo

@dataclass
class JobCreated(DomainEvent):
    job_id: int
    source_path: FileInfo

@dataclass
class JobMovedToProcessing(DomainEvent):
    job_id: int

@dataclass
class JobMovedToVerifying(DomainEvent):
    job_id: int
    output_path: FileInfo

@dataclass
class JobCompleted(DomainEvent):
    job_id: int

@dataclass
class JobFailed(DomainEvent):
    job_id: int
    reason: Optional[str] = None

@dataclass
class JobTranscodeCompleted(DomainEvent):
    job_id: int
    output_path: FileInfo