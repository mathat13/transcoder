from pydantic import BaseModel

class DispatchRequest(BaseModel):
    pass

class VerifyRequest(BaseModel):
    id: str