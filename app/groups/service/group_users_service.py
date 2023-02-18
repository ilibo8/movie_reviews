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
                user_repository = UserRepository(db)
                group = group_repository.get_group_by_name(group_name)
                group_user_repository.add_group_user(group.id, user_id)
                members_ids = group_user_repository.get_all_group_members_ids(group.id)
                owner_user_name = user_repository.get_user_name_by_user_id(group.owner_id)
                members_names = [user_repository.get_user_name_by_user_id(id) for id in members_ids]
                members_names.sort()
                return {"group_name": group_name, "owner_user_name": owner_user_name,
                        "description": group.description, "date_created": group.date_created,
                        "group_users": members_names}
        except GroupNotFound as err:
            raise GroupNotFound(err.message)
        except DuplicateEntry as err:
            raise err
        except IntegrityError as err:
            raise err

    @staticmethod
    def get_all_joined() -> list[dict]:
        """Method for getting all groups and their users"""
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            user_repository = UserRepository(db)
            group_repository = GroupRepository(db)
            all_groups = group_repository.get_all()
            all_groups_and_members = []
            for group in all_groups:
                group_name = group_repository.get_group_name_by_id(group.id)
                owner_user_name = user_repository.get_user_name_by_user_id(group.owner_id)
                members_ids = group_user_repository.get_all_group_members_ids(group.id)
                members_names = [user_repository.get_user_name_by_user_id(id) for id in members_ids]
                members_names.sort()
                all_groups_and_members.append({"group_name": group_name, "owner_user_name": owner_user_name,
                                               "description": group.description, "date_created": group.date_created,
                                               "group_users": members_names})
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
