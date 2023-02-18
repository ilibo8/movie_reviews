from pydantic import BaseModel, StrictStr


class GenreSchema(BaseModel):
    name: StrictStr

    class Config:
        orm_mode = True


