from pydantic import BaseModel


class RecommendationSchema(BaseModel):
    id : int
    group_user_id : int
    post : str

    class Config:
        orm_mode = True


class RecommendationSchemaIn(BaseModel):
    group_user_id : int
    post : str


class UsersPostsSchema(BaseModel):
    post_id : int
    post : str
