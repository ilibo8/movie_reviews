"""Module for Group services"""
from app.db import SessionLocal
from app.groups.exceptions import GroupNotFound
from app.groups.repository import GroupRepository


class GroupService:
    """Class for Group service"""

    @staticmethod
    def add_group(group_name: str, group_owner_id, description: str):
        """Method for adding new group"""
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
            return group_repository.add_group(group_name, group_owner_id, description)
        except Exception as err:
            raise err

    @staticmethod
    def get_all():
        """Method for getting all groups"""
        with SessionLocal() as db:
            group_repository = GroupRepository(db)
            groups = group_repository.get_all()
            return groups

    @staticmethod
    def delete_by_id(group_id: int):
        """Method for deleting group by id"""
        try:
            with SessionLocal() as db:
                group_repository = GroupRepository(db)
                if group_repository.delete_group_by_id(group_id):
                    return True
                raise GroupNotFound(f"No group with id {group_id}")
        except Exception as err:
            raise err
