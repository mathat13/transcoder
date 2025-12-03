from enum import Enum

class JobStatus(Enum):
    pending = "pending"
    processing = "processing"
    verifying = "verifying"
    success = "success"
    error = "error"