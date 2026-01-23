from dataclasses import dataclass
from typing import Optional
from uuid import UUID

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
    reason: Optional[str] = None

@dataclass(kw_only=True)
class TranscodeSuccess(ApplicationEvent):
    job_id: UUID