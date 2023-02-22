"""Module for Reviews schemas"""
from pydantic import BaseModel, Field, typing

from app.movie.schema import MovieOnlyTitleSchema
from app.users.schema import UserOnlyNameSchema


class ReviewSchema(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating_number: int
    review: str

    class Config:
        orm_mode = True


class ReviewSchemaOut(BaseModel):
    movie: MovieOnlyTitleSchema
    user: UserOnlyNameSchema
    rating_number: int
    review: str

    class Config:
        orm_mode = True


class ReviewSchemaIn(BaseModel):
    movie_name: str
    rating_number: int = Field(gt=0, le=10)
    review: str


class MovieAverageAndCountSchema(BaseModel):
    title: str
    director: str
    release_year: int
    country_of_origin: str
    average_rating: typing.Union[float, None]
    number_of_ratings: int

    class Config:
        orm_mode = True


class ReviewSchemaChangeRating(BaseModel):
    movie_name: str
    rating_number: int = Field(gt=0, le=10)


class TopMoviesSchema(BaseModel):
    rank : int
    movie: MovieAverageAndCountSchema

    class Config:
        orm_mode = True
