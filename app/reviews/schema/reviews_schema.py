from pydantic import BaseModel, UUID4


class ReviewSchema(BaseModel):
    id : int
    movie_id : int
    user_id : UUID4
    rating_number : int
    rating_description : str

    class Config:
        orm_mode = True


class ReviewSchemaIn(BaseModel):
    movie_id : int
    user_id : UUID4
    rating_number : int
    rating_description : str

    # @validator("rating_number")
    # def rating_number_validator(cls, value):
    #     if 10 < value < 0:
    #         raise ValueError("Rating must be in range 0-10.")
    #     return value

    class Config:
        orm_mode = True
