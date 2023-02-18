"""Module for Group services"""
from typing import Type

from app.db import SessionLocal
from app.groups.exceptions import GroupNotFound, Unauthorized
from app.groups.model import Group
from app.groups.repository import GroupRepository
from app.users.repository import UserRepository


class GroupService:
    """Class for Group service"""

    @staticmethod
    def add_group(group_name: str, group_owner_id, description: str):
        """Method for adding new group"""
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
                user_repository = UserRepository(db)
                group = group_repository.add_group(group_name, group_owner_id, description)
                owner_name = user_repository.get_user_name_by_user_id(group_owner_id)
                return {"group_name": group.group_name, "owner_user_name": owner_name,
                        "description": group.description, "date_created": group.date_created}
        except Exception as err:
            raise err

    @staticmethod
    def get_all() -> list:
        """Method for getting all groups"""
        with SessionLocal() as db:
            group_repository = GroupRepository(db)
            user_repository = UserRepository(db)
            groups = group_repository.get_all()
            all_groups = []
            for group in groups:
                owner_name = user_repository.get_user_name_by_user_id(group.owner_id)
                all_groups.append({"group_name": group.group_name, "owner_user_name": owner_name,
                                   "description": group.description, "date_created": group.date_created})
            return all_groups

    @staticmethod
    def get_group_by_name(group_name: str) -> Type[Group]:
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
                group = group_repository.get_group_by_name(group_name)
                if group is None:
                    raise GroupNotFound(f"There is no group named {group_name}")
                return group
        except Exception as err:
            raise err

    @staticmethod
    def change_group_name(group_name: str, new_name: str, user_id: int):
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
                group = group_repository.get_group_by_name(group_name)
                user_repository = UserRepository(db)
                if group is None:
                    raise GroupNotFound(f"There is no group with name {group_name}")
                if group.owner_id == user_id:
                    group2 = group_repository.change_group_name(group_name, new_name)
                    owner_name = user_repository.get_user_name_by_user_id(group2.owner_id)
                    return {"group_name": group2.group_name, "owner_user_name": owner_name,
                            "description": group2.description, "date_created": group2.date_created}
                else:
                    raise Unauthorized("Access error. Only group owner can make changes.")
        except GroupNotFound as err:
            raise GroupNotFound(err.message)

    @staticmethod
    def delete_by_id(group_name: str):
        """Method for deleting group by id"""
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
                group = group_repository.get_group_by_name(group_name)
                if group is None:
                    raise GroupNotFound(f"There is no group with name {group_name}")
                if group_repository.delete_group_by_id(group.id):
                    return True
                raise GroupNotFound(f"There is no group with that id")
        except Exception as err:
            raise err
