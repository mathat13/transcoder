from uuid import UUID
from typing import Callable, Optional

from application import (
    VerifyJobResult,
    DispatchJobResult,
)

class FakeJobService:
    verify_job_fn: Optional[Callable[[UUID], VerifyJobResult]]
    dispatch_job_fn: Optional[Callable[..., DispatchJobResult]]
    
    def __init__(self):
        self.verify_job_fn = None
        self.dispatch_job_fn = None

    def verify_job(self, job_id: UUID) -> VerifyJobResult:
        if self.verify_job_fn is None:
            raise NotImplementedError("verify_job_fn not configured")
        return self.verify_job_fn(job_id)
    
    def dispatch_job(self) -> DispatchJobResult:
        if self.dispatch_job_fn is None:
            raise NotImplementedError("dispatch_job_fn not configured")
        return self.dispatch_job_fn()