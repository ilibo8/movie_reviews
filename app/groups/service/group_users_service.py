"""Module for GroupUser services"""
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.groups.exceptions import DuplicateEntry, GroupNotFound
from app.groups.repository import GroupUserRepository, GroupRepository
from app.users.repository import UserRepository


class GroupUserService:
    """Class for GroupUser service"""

    @staticmethod
    def add_group_user(group_name: str, user_id: int):
        """Method for adding new group user"""
        try:
            with SessionLocal() as db:
                group_user_repository = GroupUserRepository(db)
                group_repository = GroupRepository(db)
                group_id = group_repository.get_group_id_by_name(group_name)
                return group_user_repository.add_group_user(group_id, user_id)
        except GroupNotFound as err:
            raise GroupNotFound(err.message)
        except DuplicateEntry as err:
            raise err
        except IntegrityError as err:
            raise err

    @staticmethod
    def get_all_joined() -> dict:
        """Method for getting all groups and their users"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            group_ids = group_user_repository.get_all_group_ids()
            user_repo = UserRepository(db)
            group_repo = GroupRepository(db)
            all_groups_and_members = {}
            for group_id in group_ids:
                members_ids = group_user_repository.get_all_group_members_ids(group_id)
                members_names = [user_repo.get_user_name_by_user_id(id) for id in members_ids]
                all_groups_and_members[group_repo.get_group_name_by_id(group_id)] = members_names
            return all_groups_and_members

    @staticmethod
    def get_all_group_members(group_id: int):
        """Method for getting all group members by group id"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            return group_user_repository.get_all_group_members_ids(group_id)


    @staticmethod
    def delete_group_user(group_id: int, user_id: int):
        """Method for deleting group user by ids"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            return group_user_repository.delete_group_user(group_id, user_id)
