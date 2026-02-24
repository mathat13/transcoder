from dataclasses import dataclass
from typing import Optional
from uuid import UUID
#from datetime import datetime

from application.workflow_engine.FailureReason import FailureReason

from domain import Event, FileInfo

@dataclass(kw_only=True)
class ApplicationEvent(Event):
    pass

@dataclass(kw_only=True)
class TranscodeVerified(ApplicationEvent):
    job_id: UUID
    transcode_file: FileInfo

@dataclass(kw_only=True)
class TranscodeVerificationFailed(ApplicationEvent):
    job_id: UUID
    transcode_file: FileInfo
    reason: Optional[FailureReason] = None

@dataclass(kw_only=True)
class TranscodeSuccess(ApplicationEvent):
    job_id: UUID

@dataclass(kw_only=True)
class JobCompletionSuccess(ApplicationEvent):
    job_id:UUID

@dataclass(kw_only=True)
class JobCompletionFailure(ApplicationEvent):
    job_id: UUID
    reason: Optional[FailureReason] = None

@dataclass(kw_only=True)
class RetryScheduled(ApplicationEvent):
    original_event: Event
    #attempt: int
    #max_attempts: int
    #scheduled_for: datetime
    #reason: str