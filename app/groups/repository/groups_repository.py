"""Modul for Group repository."""
from typing import Type
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.groups.exceptions import DuplicateEntry
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

    def delete_group_by_id(self, group_id: int) -> bool:
        """Method for deleting group by id."""
        group = self.db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            return False
        self.db.delete(group)
        self.db.commit()
        return True
