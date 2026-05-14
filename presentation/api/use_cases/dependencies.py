from domain import OperationContext

def get_job_service():
    raise NotImplementedError

def build_operation_context() -> OperationContext:
    return OperationContext.create()