from uuid import UUID
from typing import Callable, Optional

from domain import OperationContext

from application import (
    VerifyJobResult,
    DispatchJobResult,
    CreateJobResult,
)

from application import (
    CreateJobCommand,
)

class FakeJobService:
    verify_job_fn: Optional[Callable[[UUID, OperationContext], VerifyJobResult]]
    create_job_fn: Optional[Callable[[CreateJobCommand, OperationContext], CreateJobResult]]
    dispatch_job_fn: Optional[Callable[[OperationContext], DispatchJobResult]]
    
    def __init__(self):
        self.last_cmd = None
        self.last_ctx = None

        self.create_job_calls = 0
        self.dispatch_job_calls = 0
        self.verify_job_calls = 0

        self.verify_job_fn = None
        self.dispatch_job_fn = None
        self.create_job_fn = None

    def verify_job(self, job_id: UUID, ctx: OperationContext) -> VerifyJobResult:
        self.last_ctx = ctx
        self.verify_job_calls += 1

        if self.verify_job_fn is None:
            raise NotImplementedError("verify_job_fn not configured")
        return self.verify_job_fn(job_id, ctx)
    
    def dispatch_job(self, ctx: OperationContext) -> DispatchJobResult:
        self.last_ctx = ctx
        self.dispatch_job_calls += 1

        if self.dispatch_job_fn is None:
            raise NotImplementedError("dispatch_job_fn not configured")
        return self.dispatch_job_fn(ctx)
    
    def create_job(self, cmd: CreateJobCommand, ctx: OperationContext) -> CreateJobResult:
        self.last_cmd = cmd
        self.last_ctx = ctx
        self.create_job_calls += 1
        
        if self.create_job_fn is None:
            raise NotImplementedError("create_job_fn not configured")
        return self.create_job_fn(cmd, ctx)