from pydantic import BaseModel

class RescanMovieRequest(BaseModel):
    name: str = "RescanMovie"
    movieId: int