from application.workflow_engine.FailureInfo import FailureInfo
from application.workflow_engine.FailureReason import FailureReason
from application.workflow_engine.EXCEPTION_REASON_MAP import EXCEPTION_REASON_MAP
from application.exceptions.RootExceptions import RetryableException

class FailureClassifier:
    def classify(self, exc: Exception) -> FailureInfo:
        for exception_type, reason in EXCEPTION_REASON_MAP.items():
            if isinstance(exc, exception_type):
                return FailureInfo(
                    reason=reason,
                    retryable=isinstance(exc, RetryableException),
                    detail=str(exc),
                )
        
        # No matches
        return FailureInfo(
            reason=FailureReason.UNKNOWN,
            retryable=isinstance(exc, RetryableException),
            detail=str(exc),
        )
