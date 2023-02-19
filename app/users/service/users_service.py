"""Module for User services"""
import hashlib
from app.db.database import SessionLocal
from app.users.exceptions import UserInvalidPassword, UserNotFound
from app.users.repository import UserRepository


class UserService:
    """Class for User service methods"""
    @staticmethod
    def create_user(user_name: str, password: str, email: str):
        """
        The create_user function creates a new user in the database.
        It takes three parameters:
            - user_name: The name of the new user.
            - password: The password for the new user. This is hashed before being stored in the database.
            - email: The email address of the new user.
        """
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                hashed_password = hashlib.sha256(bytes(password, "utf-8")).hexdigest()
                return user_repository.create_user(user_name, hashed_password, email)
        except Exception as err:
            raise err

    @staticmethod
    def create_super_user(user_name: str, password: str, email: str):
        """
        The create_super_user function creates a super_user in the database.
        It takes three parameters: user_name, password, and email.
        The function returns the newly created super_user.
        """
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                hashed_password = hashlib.sha256(bytes(password, "utf-8")).hexdigest()
                return user_repository.create_super_user(user_name, hashed_password, email)
        except Exception as err:
            raise err

    @staticmethod
    def get_user_by_id(user_id: int):
        """
        The get_user_by_id function takes in a user_id and returns the User object associated with that id.
        """
        with SessionLocal() as db:
            user_repository = UserRepository(db)
            return user_repository.get_user_by_id(user_id)

    @staticmethod
    def get_all_users():
        """
        The get_all_users function returns all users in the database.
        """
        with SessionLocal() as db:
            user_repository = UserRepository(db)
            return user_repository.get_all_users()

    @staticmethod
    def delete_user_by_id(user_id: int):
        """
        The delete_user_by_id function deletes a user from the database by their ID.
        It takes in an integer as an argument, and returns a boolean value indicating whether delete
        was successful.
        """
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                return user_repository.delete_user_by_id(user_id)
        except Exception as err:
            raise err

    @staticmethod
    def login_user(user_name: str, password: str):
        """
        The login_user function is used to authenticate a user.
        It takes in two parameters, the username and password of the user.
        If the username exists in our database and if the password matches with that of our database, then we return
        a User object which contains all information about that particular user. Otherwise, we raise an exception.
        """
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                user = user_repository.get_user_by_user_name(user_name=user_name)
                if user is None:
                    raise UserNotFound(f"User name {user_name} not found.")
                if hashlib.sha256(bytes(password, "utf-8")).hexdigest() != user.password:
                    raise UserInvalidPassword(message="Invalid password for user.")
            return user
        except Exception as err:
            raise err
