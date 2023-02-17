from pydantic import BaseModel, validator, PositiveInt, Field


class ReviewSchema(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating_number: int
    review: str

    class Config:
        orm_mode = True


class ReviewSchemaIn(BaseModel):
    movie_name: str
    rating_number: int = Field(gt=0, le=10)
    review: str


class ReviewSchemaChangeRating(BaseModel):
    movie_name: str
    rating_number: int = Field(gt=0, le=10)


class ReviewSchemaOut(BaseModel):
    movie_title: str
    user_name: str
    rating_number: int
    review: str
