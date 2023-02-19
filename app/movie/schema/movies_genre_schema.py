"""Module for MovieGenreSchema"""
from pydantic import BaseModel, PositiveInt


class MovieGenreSchema(BaseModel):
    movie_id: PositiveInt
    genre_name: str

    class Config:
        orm_mode = True


class MovieGenreSchemaOut(BaseModel):
    genre_name: str

    class Config:
        orm_mode = True
