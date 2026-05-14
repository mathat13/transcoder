from pydantic import BaseModel

class JobNotFoundDTO(BaseModel):
    id: str