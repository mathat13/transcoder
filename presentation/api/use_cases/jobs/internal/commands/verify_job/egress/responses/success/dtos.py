from pydantic import BaseModel

class VerificationStartedDTO(BaseModel):
    id: str
    status: str