from pydantic import BaseModel, ConfigDict

class ManualCreateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_file: str

class Movie(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int

class MovieFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sourceFile: str

class RadarrWebhookCreateJobRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    movie: Movie
    movieFile: MovieFile
