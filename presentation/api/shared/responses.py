from pydantic import BaseModel
from typing import Generic

from typing import TypeVar

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    """
    Base response template, expected to inject a result literal attribute.
    Example response will end up looking like:
    result: Literal["result1", "result2"]
    data: ResponseDTO
    meta: dict
    """
    data: T | None = None
    meta: dict | None = None
    
class APIErrorResponse(BaseModel, Generic[T]):
    """
    Response used for 'errors', currently designed to be used to represent failed application use cases,
    where application returned correctly, just a failure case,
    currently the same design as APIResponse but defining different template as
    I expect needs of each use-case to evolve independently
    expected to be embedded inside a FastAPI HTTPException for further info.
    """
    data: T | None = None
    meta: dict | None = None