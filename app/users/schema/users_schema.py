from pydantic import BaseModel, EmailStr, UUID4


class UserSchema(BaseModel):
    id: UUID4
    user_name: str
    password: str
    email: str
    is_superuser: bool
    is_group_owner : bool

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

