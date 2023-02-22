"""Module for Recommendations schemas"""
from pydantic import BaseModel

from app.groups.schema import GroupUserNamesSchema, GroupUserNamesSchemaOut


class RecommendationSchema(BaseModel):
    id : int
    group_user : GroupUserNamesSchema
    post : str

    class Config:
        orm_mode = True


class RecommendationSchemaOut(BaseModel):
    id: int
    group_user : GroupUserNamesSchemaOut
    post : str

    class Config:
        orm_mode = True
