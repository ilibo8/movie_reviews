from datetime import date
from pydantic import BaseModel, StrictStr, validator
from pydantic.schema import datetime


class GroupSchema(BaseModel):
    id : int
    name : str
    owner_user_name : str
    description : str
    date_created : date

    @validator("date_created", pre=True)
    def parse_date_created(cls, value):
        return datetime.strptime(
            value,
            "%d-%m-%Y"
        ).date()

    class Config:
        orm_mode : True


class GroupSchemaIn(BaseModel):
    name: str
    owner_user_name: str
    description: str

    class Config:
        orm_mode: True
