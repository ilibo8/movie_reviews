"""Module for GroupUser repository"""
from typing import Type
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.groups.exceptions import DuplicateEntry
from app.groups.model import GroupUser


class GroupUserRepository:
    """Class for GroupUser repository"""
    def __init__(self, db: Session):
        self.db = db

    def add_group_user(self, group_id: int, user_id: int) -> GroupUser:
        """Method for adding group user"""
        try:
            if self.db.query(GroupUser).filter(and_(GroupUser.group_id == group_id,
                                                    GroupUser.user_id == user_id)).first() is not None:
                raise DuplicateEntry(f"Group id {group_id} already has that user.")
            group_user = GroupUser(group_id, user_id)
            self.db.add(group_user)
            self.db.commit()
            self.db.refresh(group_user)
            return group_user
        except IntegrityError as err:
            raise err

    def get_all(self) -> list[Type[GroupUser]]:
        """Method for getting all group users"""
        group_user = self.db.query(GroupUser).all()
        return group_user

    def get_all_group_members(self, group_id: int) -> list[Type[GroupUser]]:
        """Method for getting members of group by id"""
        group_members = self.db.query(GroupUser).filter(GroupUser.group_id == group_id).all()
        return group_members

    def delete_group_user(self, group_id: int, user_id: int) -> bool:
        """Method for deleting group user"""
        group_user = self.db.query(GroupUser).filter \
            (and_(GroupUser.group_id == group_id, GroupUser.user_id == user_id)).first()
        if group_user is None:
            return False
        self.db.delete(group_user)
        self.db.commit()
        return True
