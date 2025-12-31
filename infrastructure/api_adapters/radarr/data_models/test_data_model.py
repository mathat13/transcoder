from pydantic import BaseModel
from dataclasses import dataclass

class DataModelResponseValid(BaseModel):
    message: str

class DataModelResponse:
    def __init__(self):
        self.message = "hello"

class DataModelRequestWithParams:
    def __init__(self, movie_id: int):
        self.hello = "world"
        self.movie_id = movie_id

class DataModelRequest:
    def __init__(self):
        self.hello = "world"

class DataModelRequestValid(BaseModel):
    hello: str

class DataModelRequestWithParamsValid(BaseModel):
    hello: str
    movie_id: int