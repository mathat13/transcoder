from pydantic import BaseModel, ConfigDict


class DispatchRequest(BaseModel):
    pass

class VerifyRequest(BaseModel):
    id: str

class ManualCreateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_file: str

class Movie(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int

class MovieFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sourceFile: str

class RadarrWebhookCreateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    movie: Movie
    movieFile: MovieFile
