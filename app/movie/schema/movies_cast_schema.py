from pydantic import BaseModel

from app.actor.schema import ActorFullNameSchema


class MovieCastSchema(BaseModel):
    movie_id : int
    actor_id : ActorFullNameSchema

    class Config:
        orm_mode = True
