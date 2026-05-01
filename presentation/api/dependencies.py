from fastapi import APIRouter

from domain import OperationContext

def get_job_service():
    raise NotImplementedError

def build_operation_context() -> OperationContext:
    return OperationContext.create()

jobs_router = APIRouter(prefix="/jobs")