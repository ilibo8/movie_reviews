from pydantic import BaseModel, StrictStr, StrictInt


class MovieGenreSchema(BaseModel):
    movie_id :  StrictInt
    genre_name : StrictStr

    class Config:
        orm_mode = True
