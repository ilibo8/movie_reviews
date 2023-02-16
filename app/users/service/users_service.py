import hashlib
from app.db.database import SessionLocal
from app.users.exceptions import UserInvalidPassword
from app.users.repository import UserRepository


class UserService:
    @staticmethod
    def create_user(user_name: str, password: str, email: str):
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                hashed_password = hashlib.sha256(bytes(password, "utf-8")).hexdigest()
                return user_repository.create_user(user_name, hashed_password, email)
        except Exception as e:
            raise e

    @staticmethod
    def create_super_user(user_name: str, password: str, email: str):
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                hashed_password = hashlib.sha256(bytes(password, "utf-8")).hexdigest()
                return user_repository.create_super_user(user_name, hashed_password, email)
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_id(user_id: int):
        with SessionLocal() as db:
            user_repository = UserRepository(db)
            return user_repository.get_user_by_id(user_id)

    @staticmethod
    def get_all_users():
        with SessionLocal() as db:
            user_repository = UserRepository(db)
            return user_repository.get_all_users()

    @staticmethod
    def delete_user_by_id(user_id: int):
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                return user_repository.delete_user_by_id(user_id)
        except Exception as e:
            raise e

    @staticmethod
    def login_user(user_name: str, password: str):
        try:
            with SessionLocal() as db:
                user_repository = UserRepository(db)
                user = user_repository.get_user_by_user_name(user_name=user_name)
                if hashlib.sha256(bytes(password, "utf-8")).hexdigest() != user.password:
                    raise UserInvalidPassword(message="Invalid password for user.")
            return user
        except Exception as e:
            raise e
