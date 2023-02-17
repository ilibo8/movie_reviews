from pydantic import BaseModel, StrictInt, StrictStr, validator
from pydantic.types import date


class MovieSchema(BaseModel):
    id : int
    title : str
    director : str
    release_year : int
    country_of_origin : str

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
