from pydantic import BaseModel

class JobDispatchedDTO(BaseModel):
    id: str
    source_file: str
    transcode_output_file: str

class NoJobAvailableDTO(BaseModel):
    pass

