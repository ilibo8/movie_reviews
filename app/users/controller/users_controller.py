"""Module for controller layer of User"""
from fastapi import HTTPException, Response
from sqlalchemy.exc import IntegrityError
from app.users.exceptions import UserInvalidPassword, AlreadyExist, UserNotFound
from app.users.service import UserService, signJWT


class UserController:
    """Class for User controller."""
    @staticmethod
    def create_user(user_name: str, password: str, email: str):
        """
        The create_user function creates a new user in the database.
        It takes three parameters:
            - user_name: The name of the new user.
            - password: The password for the new user.
            - email: The email address of the new user.
        """
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
        """
        The create_super_user function creates a super_user in the database.
        It takes three parameters: user_name, password and email. It returns the created superuser.
        """
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
        """
        The login_user function is used to authenticate a user.
        It takes in two parameters, the username and password of the user.
        If the username and password are valid, it returns a JWT token that can be used for future requests.
        """
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
        """
        The get_user_by_id function returns a user object given an id.
        If the user does not exist, it raises an HTTPException with status code 400.
        """
        user = UserService.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=400, detail=f"User with provided id {user_id} does not exist.")
        return user

    @staticmethod
    def get_all_users():
        """
        The get_all_users function returns a list of all users in the database.
        """
        users = UserService.get_all_users()
        return users

    @staticmethod
    def delete_user_by_id(user_id: int):
        """
        The delete_user_by_id function deletes a user from the database by their id.
        It takes in an integer as an argument, and returns a string.
        """
        try:
            deleted = UserService.delete_user_by_id(user_id)
            if deleted:
                return Response(content=f"User with id - {user_id} is deleted.")
            return Response(content=f"User with id - {user_id} doesn't exist.")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))
