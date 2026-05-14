from pydantic import BaseModel

class VerifyJobSuccessDTO(BaseModel):
    id: str
    status: str