from pydantic import BaseModel

class VerifyJobDTO(BaseModel):
    id: str
    status: str

class VerifyJobErrorDTO(BaseModel):
    id: str