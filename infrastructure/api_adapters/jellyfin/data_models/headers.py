from pydantic import BaseModel, Field, ConfigDict, field_validator

class JellyfinHeaders(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    authorization: str = Field(alias="Authorization")
    accept: str = Field("application/json", alias="Accept")
    content_type: str = Field("application/json", alias="Content-Type")
    
    @field_validator("authorization", mode="before")
    @classmethod
    def add_mediabrowser_prefix(cls, value: str) -> str:
        if value.startswith("MediaBrowser Token="):
            return value
        return f"MediaBrowser Token={value}"