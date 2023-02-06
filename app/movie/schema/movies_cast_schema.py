from pydantic import BaseModel


class MovieCastSchema(BaseModel):
    movie_id : int
    actor_id : int

    class Config:
        orm_mode = True

