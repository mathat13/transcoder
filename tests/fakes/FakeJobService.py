from uuid import UUID
from typing import Callable, Optional

from domain import OperationContext

from application import (
    VerifyJobResult,
    DispatchJobResult,
    CreateJobResult,
)

from presentation import CreateJobCommand

class FakeJobService:
    verify_job_fn: Optional[Callable[[UUID], VerifyJobResult]]
    dispatch_job_fn: Optional[Callable[..., DispatchJobResult]]
    create_job_fn: Optional[Callable[[CreateJobCommand, OperationContext], CreateJobResult]]
    
    def __init__(self):
        self.last_cmd = None
        self.last_ctx = None

        self.create_job_calls = 0

        self.verify_job_fn = None
        self.dispatch_job_fn = None
        self.create_job_fn = None

    def verify_job(self, job_id: UUID) -> VerifyJobResult:
        if self.verify_job_fn is None:
            raise NotImplementedError("verify_job_fn not configured")
        return self.verify_job_fn(job_id)
    
    def dispatch_job(self) -> DispatchJobResult:
        if self.dispatch_job_fn is None:
            raise NotImplementedError("dispatch_job_fn not configured")
        return self.dispatch_job_fn()
    
    def create_job(self, cmd: CreateJobCommand, ctx: Optional[OperationContext] = None) -> CreateJobResult:
        self.last_cmd = cmd
        self.last_ctx = ctx
        self.create_job_calls += 1
        
        if self.create_job_fn is None:
            raise NotImplementedError("create_job_fn not configured")
        ctx = ctx or OperationContext.create()
        return self.create_job_fn(cmd, ctx)