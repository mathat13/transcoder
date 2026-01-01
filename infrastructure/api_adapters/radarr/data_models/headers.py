from pydantic import BaseModel

class RadarrHeaders(BaseModel):
    X_Api_Key: str
    Accept: str = "application/json"
    Content_Type: str = "application/json"