from pydantic import BaseModel

class JobSummaryDTO(BaseModel):
    id: str
    source_file: str
    transcode_output_file: str
    delivery_file: str
    status: str