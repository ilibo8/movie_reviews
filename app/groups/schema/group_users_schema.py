from pydantic import BaseModel


class GroupUserSchema(BaseModel):

    group_id: int
    user_id: int

    class Config:
        orm_mode = True
