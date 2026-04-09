from dataclasses import dataclass
from typing import Optional
from uuid import UUID
#from datetime import datetime

from application.workflow_engine.FailureReason import FailureReason
from application.workflow_engine.FailureInfo import FailureInfo

from domain import Event, FileInfo

@dataclass(kw_only=True)
class ApplicationEvent(Event):
    pass

@dataclass(kw_only=True)
class TranscodeVerified(ApplicationEvent):
    job_id: UUID
    transcode_output_file: FileInfo

@dataclass(kw_only=True)
class TranscodeVerificationFailed(ApplicationEvent):
    job_id: UUID
    transcode_output_file: FileInfo
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
    failure_info: Optional[FailureInfo] = None

@dataclass(kw_only=True)
class RetryScheduled(ApplicationEvent):
    original_event: Event
    #attempt: int
    #max_attempts: int
    #scheduled_for: datetime
    #reason: str

@dataclass(kw_only=True)
class JobNotFoundDuringVerification(ApplicationEvent):
    job_id: UUID