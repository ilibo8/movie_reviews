"""Module for GroupUser schemas"""
from pydantic import BaseModel


class GroupUserSchema(BaseModel):
    id: int
    group_id: int
    user_id: int

    class Config:
        orm_mode = True
