"""Module for Recommendations schemas"""
from pydantic import BaseModel


class RecommendationSchema(BaseModel):
    id : int
    group_user_id : int
    post : str

    class Config:
        orm_mode = True
