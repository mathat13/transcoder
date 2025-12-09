from dataclasses import dataclass
from typing import Optional

@dataclass
class ApplicationEvent:
    pass

@dataclass
class TranscodeVerified(ApplicationEvent):
    job_id: int
    file_path: str

@dataclass
class TranscodeVerificationFailed(ApplicationEvent):
    job_id: int
    file_path: str
    reason: Optional[str] = None