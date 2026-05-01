from pydantic import BaseModel, ConfigDict

class ManualCreateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_file: str
