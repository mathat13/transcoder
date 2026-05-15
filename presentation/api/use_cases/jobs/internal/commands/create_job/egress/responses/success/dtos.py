from pydantic import BaseModel

class JobCreatedDTO(BaseModel):
    id: str
    status: str
    source_file: str