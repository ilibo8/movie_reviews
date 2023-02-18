from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.users.exceptions import UserInvalidPassword, AlreadyExist, UserNotFound
from app.users.service import UserService, signJWT


class UserController:
    @staticmethod
    def create_user(user_name: str, password: str, email: str):
        try:
            user = UserService.create_user(user_name, password, email)
            return user
        except AlreadyExist as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def create_super_user(user_name: str, password: str, email: str):
        try:
            user = UserService.create_super_user(user_name, password, email)
            return user
        except AlreadyExist as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def login_user(user_name: str, password: str):
        try:
            user = UserService.login_user(user_name, password)
            if user.is_superuser:
                return signJWT(user.id, "super_user")
            return signJWT(user.id, "classic_user")
        except UserNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except UserInvalidPassword as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_user_by_id(user_id: int):
        user = UserService.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=400, detail=f"User with provided id {user_id} does not exist.")
        return user

    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()
        return users

    @staticmethod
    def delete_user_by_id(user_id: int):
        try:
            deleted = UserService.delete_user_by_id(user_id)
            if deleted:
                return Response(content=f"User with id - {user_id} is deleted.")
            else:
                return Response(content=f"User with id - {user_id} doesn't exist.")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))
