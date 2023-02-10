from pydantic import BaseModel, validator
from pydantic.validators import date


class GroupSchema(BaseModel):
    id : int
    name : str
    owner_user_name : str
    description : str
    date_created : str

    # @validator("date_created", pre=True)
    # def parse_date(cls, value):
    #     return date.strptime(
    #         value,
    #         "%Y-%m-%d"
    #     ).date()

    class Config:
        orm_mode : True


class GroupSchemaIn(BaseModel):
    name: str
    owner_user_name: str
    description: str

    class Config:
        orm_mode: True
