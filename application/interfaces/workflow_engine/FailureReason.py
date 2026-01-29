from enum import Enum

class FailureReason(Enum):
        TRANSIENT_IO = "transient_io"
        PERMISSION_DENIED = "permission_denied"
        INVALID_INPUT = "invalid_input"
        EXTERNAL_SERVICE_FAILURE = "external_service_failure"
        NON_RETRYABLE = "non_retryable"