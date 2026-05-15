from pydantic import BaseModel, ConfigDict

class CreateJobRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_file: str