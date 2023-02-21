"""Module for Users schemas"""
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    user_name: str
    password: str
    email: str
    is_superuser: bool

    class Config:
        orm_mode = True


class UserSchemaIn(BaseModel):
    user_name: str
    password: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    user_name: str
    password: str

    class Config:
        orm_mode = True


class UserOnlyNameSchema(BaseModel):
    user_name: str

    class Config:
        orm_mode = True
