"""Module for GroupUser schemas"""
from pydantic import BaseModel

from app.groups.schema import GroupSchema
from app.users.schema import UserIdNameSchema


class GroupUserNamesSchemaOut(BaseModel):
    id: int
    user: UserIdNameSchema
    movie_group: GroupSchema

    class Config:
        orm_mode = True
