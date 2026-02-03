from enum import Enum

class FailureReason(Enum):
        API_CALL_FAILURE = "api_call_failure"
        FILESYSTEM_LOGIC = "filesystem_logic"
        FILESYSTEM_IO = "filesystem_io"
        UNKNOWN = "unknown"