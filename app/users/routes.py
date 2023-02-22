from fastapi import APIRouter, Depends
from app.users.controller import UserController
from app.users.controller.user_auth_controller import JWTBearer
from app.users.schema import UserLoginSchema, UserSchema, UserSchemaIn

user_router = APIRouter(prefix="/api/users", tags=["superuser - Users"])
login_router = APIRouter(prefix="/api/login", tags=["Login"])
register_router = APIRouter(prefix="/api/users", tags=["Signup"])


@login_router.post("/")
def login_for_access_token(user: UserLoginSchema):
    """
    The function is used to log in a user and return an access token.
    """
    return UserController.login_user(user.user_name, user.password)


@register_router.post("/create-user", response_model=UserSchema)
def create_user(user: UserSchemaIn):
    """
    The function creates a new user in the database.
    """
    return UserController.create_user(user.user_name, user.password, user.email)


@user_router.post("/add-super-user", response_model=UserSchema, dependencies=[Depends(JWTBearer("super_user"))])
def create_super_user(user: UserSchemaIn):
    """
    The function creates a super_user in the database.
    """
    return UserController.create_super_user(user.user_name, user.password, user.email)


@user_router.get("/id/{user_id}", response_model=UserSchema, dependencies=[Depends(JWTBearer("super_user"))])
def get_user_by_id(user_id: int):
    """
    The function takes a user_id as an argument and returns the user associated with that id.
    """
    return UserController.get_user_by_id(user_id)


@user_router.get("/get-all-users", response_model=list[UserSchema], dependencies=[Depends(JWTBearer("super_user"))])
def get_all_users():
    """
    The function returns a list of all users in the database.
    """
    return UserController.get_all_users()


@user_router.delete("/{user_id}", dependencies=[Depends(JWTBearer("super_user"))])
def delete_user_by_id(user_id: int):
    """
    The function deletes a user from the database by their ID.
    """
    return UserController.delete_user_by_id(user_id)
