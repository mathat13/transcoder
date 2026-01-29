from enum import Enum

class FailureReason(Enum):
        EXTERNAL_SERVICE_FAILURE = "external_service_failure"
        API_CALL_FAILURE = "api_call_failure"
        FILESYSTEM_LOGIC = "filesystem_logic"
        FILESYSTEM_IO = "filesystem_io"
        UNKNOWN = "unknown"