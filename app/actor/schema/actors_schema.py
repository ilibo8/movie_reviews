"""Module for schemas for actors table"""
from pydantic import BaseModel, StrictStr


class ActorSchema(BaseModel):
    id : int
    full_name : str
    nationality : str

    class Config:
        orm_mode = True


class ActorSchemaIn(BaseModel):
    full_name: StrictStr
    nationality: StrictStr

    class Config:
        orm_mode = True


class ActorSchemaOut(BaseModel):
    full_name: str

    class Config:
        orm_mode = True
