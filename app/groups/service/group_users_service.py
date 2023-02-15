"""Module for GroupUser services"""
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.groups.exceptions import DuplicateEntry
from app.groups.repository import GroupUserRepository


class GroupUserService:
    """Class for GroupUser service"""

    @staticmethod
    def add_group_user(group_id: int, user_id: int):
        """Method for adding new group user"""
        try:
            with SessionLocal() as db:
                group_user_repository = GroupUserRepository(db)
            return group_user_repository.add_group_user(group_id, user_id)
        except DuplicateEntry as err:
            raise err
        except IntegrityError as err:
            raise err

    @staticmethod
    def get_all():
        """Method for getting all groups and their users"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            return group_user_repository.get_all()

    @staticmethod
    def get_all_group_members(group_id: int):
        """Method for getting all group members by group id"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            return group_user_repository.get_all_group_members(group_id)

    @staticmethod
    def delete_group_user(group_id: int, user_id: int):
        """Method for deleting group user by ids"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            return group_user_repository.delete_group_user(group_id, user_id)
