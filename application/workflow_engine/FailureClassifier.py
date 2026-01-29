from application.workflow_engine.FailureInfo import FailureInfo
from application.workflow_engine.FailureReason import FailureReason
from application.exceptions.ServiceExceptions import *

class FailureClassifier():
    def classify(self, exc: Exception) -> "FailureInfo":
        if isinstance(exc, FileSystemIOError):
            return FailureInfo(
                reason=FailureReason.FILESYSTEM_IO,
                retryable=exc.retryable,
                detail=str(exc),
            )
        
        if isinstance(exc, FileSystemException):
            return FailureInfo(
                reason=FailureReason.FILESYSTEM_LOGIC,
                retryable=exc.retryable,
                detail=str(exc),
            )
        
        if isinstance(exc, APIServiceException):
            return FailureInfo(
                reason=FailureReason.API_CALL_FAILURE,
                retryable=exc.retryable,
                detail=str(exc),
            )
        
        return FailureInfo(
            reason=FailureReason.UNKNOWN,
            retryable=getattr(exc, "retryable", False),
            detail=str(exc),
        )
