from dataclasses import dataclass

from application.workflow_engine.FailureReason import FailureReason

@dataclass(frozen=True)
class FailureInfo:
    reason: FailureReason
    retryable: bool
    detail: str