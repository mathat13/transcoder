from pydantic import BaseModel, Field, ConfigDict

class RadarrHeaders(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    x_api_key: str = Field(..., alias="X-Api-Key")
    accept: str = Field("application/json", alias="Accept")
    content_type: str = Field("application/json", alias="Content-Type")