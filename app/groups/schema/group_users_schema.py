"""Module for GroupUser schemas"""
from pydantic import BaseModel

from app.groups.schema import GroupSchema, GroupOnlyNameSchema
from app.users.schema import UserIdNameSchema, UserOnlyNameSchema


class GroupUserNamesSchema(BaseModel):
    id: int
    user: UserIdNameSchema
    movie_group: GroupSchema

    class Config:
        orm_mode = True


class GroupUserNamesSchemaOut(BaseModel):
    user: UserOnlyNameSchema
    movie_group: GroupOnlyNameSchema

    class Config:
        orm_mode = True
