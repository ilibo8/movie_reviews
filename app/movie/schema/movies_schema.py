import typing
from pydantic import BaseModel, StrictInt
from pydantic.schema import date
from app.actor.schema import ActorFullNameSchema
from app.genre.schema import GenreSchema


class MovieSchema(BaseModel):
    id : int
    title : str
    director : str
    movie_cast : typing.List[ActorFullNameSchema]
    genre : typing.List[GenreSchema]
    release_year : int
    country_of_origin : str

    class Config:
        orm_mode = True


class MovieSchemaIn(BaseModel):
    title: str
    director: str
    movie_cast: typing.List[ActorFullNameSchema]
    genre: typing.List[GenreSchema]
    release_year: StrictInt
    country_of_origin: str

    class Config:
        orm_mode = True
