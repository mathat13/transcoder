from pydantic import BaseModel

class VerifyRequest(BaseModel):
    id: str