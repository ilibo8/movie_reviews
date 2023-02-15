"""Modul for Group repository."""
from typing import Type
from sqlalchemy.orm import Session
from app.groups.exceptions import DuplicateEntry, GroupNotFound
from app.groups.model import Group


class GroupRepository:
    """Group repository class."""

    def __init__(self, db: Session):
        self.db = db

    def add_group(self, group_name: str, owner_id: int, description: str) -> Group:
        """Method for adding new group."""
        group = Group(group_name=group_name, owner_id=owner_id, description=description)
        if self.db.query(Group).filter(Group.group_name == group_name).first() is not None:
            raise DuplicateEntry("Group name already used, try another one.")
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def get_all(self) -> list[Type[Group]]:
        """Method for getting all groups."""
        groups = self.db.query(Group).all()
        return groups

    def get_group_by_name(self, group_name: str) -> Type[Group] | None:
        group = self.db.query(Group).filter(Group.group_name == group_name).first()
        return group

    def get_group_name_by_id(self, group_id: int) -> str:
        if self.db.query(Group).filter(Group.id == group_id).first() is None:
            raise GroupNotFound(f"There is no group with id {group_id}")
        name = self.db.query(Group.group_name).filter(Group.id == group_id).first()
        return name[0]

    def get_group_id_by_name(self, group_name: str) -> int:
        if self.db.query(Group).filter(Group.group_name == group_name).first() is None:
            raise GroupNotFound(f"There is no group named {group_name}")
        group_id = self.db.query(Group.id).filter(Group.group_name == group_name).first()
        return group_id[0]

    def change_group_name(self, group_name: str, new_name: str):
        group = self.db.query(Group).filter(Group.group_name == group_name).first()
        if group is None:
            raise GroupNotFound(f"There is no group with name {group_name}.")
        if self.db.query(Group).filter(Group.group_name == new_name).first() is not None:
            raise DuplicateEntry("Group name already used, try another one.")
        group.group_name = new_name
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete_group_by_id(self, group_id: int) -> bool:
        """Method for deleting group by id."""
        group = self.db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise GroupNotFound(f"There is no group with that id")
        self.db.delete(group)
        self.db.commit()
        return True
