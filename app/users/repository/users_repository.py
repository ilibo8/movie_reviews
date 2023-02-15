from typing import Type
from sqlalchemy.orm import Session

from app.users.exceptions import UserNotFound, AlreadyExist
from app.users.model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_name: str, password: str, email: str) -> User:
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
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

    def get_user_name_by_user_id(self, user_id: int):
        user = self.db.query(User.user_name).filter(User.id == user_id).first()
        return user[0]

    def get_user_by_user_name(self, user_name: str) -> Type[User] | None:
        user = self.db.query(User).filter(User.user_name == user_name).first()
        if user is None:
            raise UserNotFound(f"User name {user_name} not found.")
        return user

    def get_all_users(self) -> list[Type[User]]:
        users = self.db.query(User).all()
        return users

    def delete_user_by_id(self, user_id: int) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
