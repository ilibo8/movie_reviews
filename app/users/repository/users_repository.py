"""Module for User repository"""
from typing import Type
from sqlalchemy.orm import Session
from app.users.exceptions import AlreadyExist, UserNotFound
from app.users.model import User


class UserRepository:
    """Class for User repository"""
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_name: str, password: str, email: str) -> User:
        """
        The create_user function creates a new user in the database.
        It takes three parameters: user_name, password and email.
        If the username already exists in the database, it raises an AlreadyExist exception.
        If the email address already exists in the database, it raises an AlreadyExist exception.
        """
        user = User(user_name, password, email)
        if self.db.query(User).filter(User.user_name == user_name).first() is not None:
            raise AlreadyExist(f"User name {user_name} already exist.")
        if self.db.query(User).filter(User.email == email).first() is not None:
            raise AlreadyExist(f"Email {email} already exist.")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_super_user(self, user_name: str, password : str, email: str) -> User:
        """
        The create_super_user function creates a new user with the given username, password, and email.
        If the username already exists in the database then AlreadyExist is raised. If the email address
        is already used by another user in our database then AlreadyExist is also raised.
        """
        user = User(user_name=user_name, password=password, email=email, is_superuser=True)
        if self.db.query(User).filter(User.user_name == user_name).first() is not None:
            raise AlreadyExist(f"User name {user_name} already exist.")
        if self.db.query(User).filter(User.email == email).first() is not None:
            raise AlreadyExist(f"Email {email} already exist.")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> Type[User] | None:
        """
        The get_user_by_id function accepts a user_id as an argument and returns the User object associated
        with that id. If no such User exists, it returns None.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def get_user_name_by_user_id(self, user_id: int) -> str:
        """
        The get_user_name_by_user_id function takes a user_id as an argument and returns the corresponding user_name.
        It queries the database for a User object with matching id, then returns that User's username.
        """
        user = self.db.query(User.user_name).filter(User.id == user_id).first()
        return user[0]

    def get_user_by_user_name(self, user_name: str) -> Type[User] | None:
        """
        The get_user_by_user_name function takes a user_name as an argument and returns the User object associated
        with that user_name. If no such user exists, it raises a UserNotFound exception.
        """
        user = self.db.query(User).filter(User.user_name == user_name).first()
        if user is None:
            raise UserNotFound(f"User with name {user_name} not found.")
        return user

    def get_all_users(self) -> list[Type[User]]:
        """
        The get_all_users function returns a list of all the users in the database.
        """
        users = self.db.query(User).all()
        return users

    def delete_user_by_id(self, user_id: int) -> bool:
        """
        The delete_user_by_id function deletes a user from the database.
        It takes in an integer representing the id of the user to be deleted and returns True if it was successful,
        False otherwise.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
