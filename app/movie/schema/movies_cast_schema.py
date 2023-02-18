from pydantic import BaseModel, PositiveInt

from app.actor.schema import ActorSchemaOut


class MovieCastSchema(BaseModel):
    movie_id : PositiveInt
    actor_id : PositiveInt

    class Config:
        orm_mode = True


class MovieCastSchemaOut(BaseModel):
    actor_id : int
    actor : ActorSchemaOut

    class Config:
        orm_mode = True
