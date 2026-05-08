from pydantic import BaseModel
from typing import Generic

from typing import TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """
    Base response template, expected to inject a result literal attribute.
    Example response will end up looking like:
    result: Literal["result1", "result2"]
    data: ResponseDTO
    meta: dict
    """
    data: T | None = None
    meta: dict | None = None
    
class ErrorResponse(BaseModel):
    """
    Response used for 'errors',
    expected to be embedded inside a FastAPI HTTPException for further info."""
    error: str
    message: str | None = None
    job_id: str | None = None
    details: dict | None = None