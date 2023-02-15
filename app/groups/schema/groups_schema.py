from pydantic import BaseModel
from pydantic.types import date


class GroupSchema(BaseModel):
    id: int
    group_name: str
    owner_id : int
    description: str
    date_created: date

    class Config:
        orm_mode = True


class GroupSchemaIn(BaseModel):
    group_name: str
    description: str

    class Config:
        orm_mode = True
