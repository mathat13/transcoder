from pydantic import BaseModel, ConfigDict

class Movie(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int

class MovieFile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    sourceFile: str

class CreateJobRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    movie: Movie
    movieFile: MovieFile
    eventType: str