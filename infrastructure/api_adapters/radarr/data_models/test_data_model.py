from pydantic import BaseModel

class DataModelResponse(BaseModel):
    message: str = "hello"

class DataModelRequestWithParams(BaseModel):
    hello: str = "world"
    movie_id: int

class DataModelRequest(BaseModel):
    hello: str = "world"