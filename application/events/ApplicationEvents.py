from dataclasses import dataclass
from typing import Optional

from domain import Event

@dataclass(kw_only=True)
class ApplicationEvent(Event):
    pass

@dataclass(kw_only=True)
class TranscodeVerified(ApplicationEvent):
    job_id: int
    file_path: str

@dataclass(kw_only=True)
class TranscodeVerificationFailed(ApplicationEvent):
    job_id: int
    file_path: str
    reason: Optional[str] = None