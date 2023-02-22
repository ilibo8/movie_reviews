"""Module for Movies schemas"""
from pydantic import BaseModel, StrictInt, StrictStr, validator
from pydantic.types import date, PositiveInt
from app.movie.schema import MovieCastSchemaOut, MovieGenreSchemaOut


class MovieSchema(BaseModel):
    id: int
    title: str
    director: str
    release_year: int
    country_of_origin: str

    class Config:
        orm_mode = True


class MovieSchemaOut(BaseModel):
    title: str
    director: str
    release_year: int
    country_of_origin: str

    class Config:
        orm_mode = True


class MovieSchemaJoined(BaseModel):
    title: str
    director: str
    release_year: int
    country_of_origin: str

    actors: list
    genre: list

    class Config:
        orm_mode = True


class MovieSchemaIn(BaseModel):
    title: str
    director: StrictStr
    release_year: StrictInt
    country_of_origin: StrictStr

    @validator("release_year")
    def release_year_validator(cls, value):
        if value < 1895:
            raise ValueError("Year cannot be less than 1895.")
        if value > date.today().year:
            raise ValueError("Year cannot be greater than current.")
        return value

    class Config:
        orm_mode = True


class MovieSchemaAll(BaseModel):
    id: int
    title: str
    director: StrictStr
    release_year: StrictInt
    country_of_origin: StrictStr

    movie_cast: list[MovieCastSchemaOut]
    movie_genre: list[MovieGenreSchemaOut]

    class Config:
        orm_mode = True


class MovieSchemaUpdateTitle(BaseModel):
    id: PositiveInt
    title: str

    class Config:
        orm_mode = True


class MovieSchemaUpdateDirector(BaseModel):
    id: PositiveInt
    director: StrictStr

    class Config:
        orm_mode = True


class MovieSchemaUpdateReleaseYear(BaseModel):
    id: PositiveInt
    release_year: StrictInt

    @validator("release_year")
    def release_year_validator(cls, value):
        if value < 1895:
            raise ValueError("Year cannot be less than 1895.")
        if value > date.today().year:
            raise ValueError("Year cannot be greater than current.")
        return value

    class Config:
        orm_mode = True


class MovieOnlyTitleSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True
