"""Modul for Group repository."""
from typing import Type
from sqlalchemy.orm import Session
from app.groups.exceptions import DuplicateEntry, GroupNotFound
from app.groups.model import Group, GroupUser


class GroupRepository:
    """Group repository class."""

    def __init__(self, db: Session):
        self.db = db

    def add_group(self, group_name: str, owner_id: int, description: str) -> Group:
        """
        The add_group function creates a new group in the database.
        """
        group = Group(group_name=group_name, owner_id=owner_id, description=description)
        if self.db.query(Group).filter(Group.group_name == group_name).first() is not None:
            raise DuplicateEntry("Group name already used, try another one.")
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        group_user = GroupUser(group.id, owner_id)
        self.db.add(group_user)
        self.db.commit()
        self.db.refresh(group_user)
        return group

    def get_all(self) -> list[Type[Group]]:
        """
        The get_all function returns a list of all the groups in the database.
        """
        groups = self.db.query(Group).all()
        return groups

    def get_group_by_name(self, group_name: str) -> Type[Group] | None:
        """
        The get_group_by_name function takes a group name as an argument and returns the Group object
        corresponding to that group name. If no such Group exists, it returns None.
        """
        group = self.db.query(Group).filter(Group.group_name == group_name).first()
        if group is None:
            raise GroupNotFound(f"There is no group with name {group_name}")
        return group

    def get_groups_by_owner_id(self, user_id: int):
        """
        Returns all groups owned by user with provided id.
        """
        return self.db.query(Group).filter(Group.owner_id == user_id).all()

    def get_group_name_by_id(self, group_id: int) -> str:
        """
        The function takes a group_id as an argument and returns the name of the group with that id.
        If no such group exists, it raises a GroupNotFound exception.
        """
        if self.db.query(Group).filter(Group.id == group_id).first() is None:
            raise GroupNotFound(f"There is no group with id {group_id}")
        name = self.db.query(Group.group_name).filter(Group.id == group_id).first()
        return name[0]

    def get_group_id_by_name(self, group_name: str) -> int:
        """
        The get_group_id_by_name function takes a group name as an argument and returns the id of that group.
        If there is no such group, it raises a GroupNotFound exception.
        """
        if self.db.query(Group).filter(Group.group_name == group_name).first() is None:
            raise GroupNotFound(f"There is no group named {group_name}")
        group_id = self.db.query(Group.id).filter(Group.group_name == group_name).first()
        return group_id[0]

    def change_group_name(self, group_name: str, new_name: str):
        """
        The change_group_name function takes in a group name and a new name for the group.
        It then checks to see if the new name is already taken, and if it is not, changes the
        group's name to that of the new_name argument. It returns nothing.
        """
        group = self.db.query(Group).filter(Group.group_name == group_name).first()
        if self.db.query(Group).filter(Group.group_name == new_name).first() is not None:
            raise DuplicateEntry("Group name already used, try another one.")
        group.group_name = new_name
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete_group_by_id(self, group_id: int) -> bool:
        """
        The delete_group_by_id function deletes a group from the database.
        """
        group = self.db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise GroupNotFound("There is no group with that id")
        self.db.delete(group)
        self.db.commit()
        return True
