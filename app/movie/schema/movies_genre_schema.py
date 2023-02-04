from pydantic import BaseModel


class MovieGenreSchema(BaseModel):
    movie_id :  int
    genre_name : str

    class Config:
        orm_mode = True
