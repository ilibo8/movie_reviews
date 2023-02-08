from pydantic import BaseModel, StrictInt


class MovieCastSchema(BaseModel):
    movie_id : StrictInt
    actor_id : StrictInt

    class Config:
        orm_mode = True

