from fastapi import APIRouter, Depends
from app.users.controller import UserController
from app.users.controller.user_auth_controller import JWTBearer
from app.users.schema import *

user_router = APIRouter(prefix="/api/users", tags=["Users"])
login_router = APIRouter(prefix="/api/login", tags=["Login"])


@login_router.post("/login")
def login_for_access_token(user: UserLoginSchema):
    return UserController.login_user(user.user_name, user.password)


@user_router.post("/add-user", response_model=UserSchema)
def create_user(user: UserSchemaIn):
    return UserController.create_user(user.user_name, user.password, user.email)


@user_router.post("/add-super-user", response_model=UserSchema, dependencies=[Depends(JWTBearer("super_user"))])
def create_super_user(user: UserSchemaIn):
    return UserController.create_super_user(user.user_name, user.password, user.email)


@user_router.get("/id/{user_id}", response_model=UserSchema)
def get_user_by_id(user_id: int):
    return UserController.get_user_by_id(user_id)


@user_router.get("/get-all-users", response_model=list[UserSchema], dependencies=[Depends(JWTBearer("super_user"))])
def get_all_users():
    return UserController.get_all_users()


@user_router.delete("/{user_id}", dependencies=[Depends(JWTBearer("super_user"))])
def delete_user_by_id(user_id: int):
    return UserController.delete_user_by_id(user_id)



