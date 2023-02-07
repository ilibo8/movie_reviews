from pydantic import BaseModel, StrictInt, StrictStr

from app.movie.schema import MovieCastSchema, MovieGenreSchema


class MovieSchema(BaseModel):
    id : int
    title : str
    director : str
    release_year : int
    country_of_origin : str

    movie_cast : MovieCastSchema
    movie_genre : MovieGenreSchema

    class Config:
        orm_mode = True


class MovieSchemaJoined(BaseModel):
    id : int
    title : str
    director : str
    release_year : int
    country_of_origin : str

    actors: list
    genre: list

    class Config:
        orm_mode = True


class MovieSchemaIn(BaseModel):
    title: StrictStr
    director: StrictStr
    release_year: StrictInt
    country_of_origin: StrictStr

    class Config:
        orm_mode = True
