from pydantic import BaseModel, Field
from typing import Generic
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R", bound=BaseModel)

from presentation.api.use_cases.common.dtos import EmptyData

class APISuccessResponse(BaseModel, Generic[T]):
    """
    Base response template, expected to inject a result literal attribute.
    Example response will end up looking like:
    result: Literal["result1", "result2"]
    data: SuccessResponseDTO
    meta: dict
    """
    data: T | EmptyData = Field(default_factory=EmptyData)
    meta: dict = Field(default_factory=dict)
    
class APIFailureResponse(BaseModel, Generic[T]):
    """
    Response used for 'errors', currently designed to be used to represent failed application use cases,
    where application returned correctly, just a failure case,
    currently the same design as APIResponse but defining different template as
    I expect needs of each use-case to evolve independently
    expected to be embedded inside a FastAPI HTTPException for further info. Format:
    error: Literal["result1", "result2"]
    data: FailureResponseDTO
    meta: dict
    """
    data: T | None = None
    meta: dict | None = None

class HTTPPresentation(BaseModel, Generic[R]):
    status_code: int
    response: R