from pydantic import BaseModel

class DispatchRequest(BaseModel):
    pass

class VerifyRequest(BaseModel):
    id: str

class ManualCreateRequest(BaseModel):
    source_file: str