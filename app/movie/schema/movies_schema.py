from pydantic import BaseModel, StrictInt
from app.movie.schema import MovieCastSchema, MovieGenreSchema


class MovieSchema(BaseModel):
    id : int
    title : str
    director : str
    release_year : int
    country_of_origin : str

    movie_cast: list[MovieCastSchema.actor_id]
    movie_genre: list[MovieGenreSchema.genre_name]

    class Config:
        orm_mode = True


class MovieSchemaIn(BaseModel):
    title: str
    director: str
    release_year: StrictInt
    country_of_origin: str

    class Config:
        orm_mode = True
