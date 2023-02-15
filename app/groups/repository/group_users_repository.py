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
                raise DuplicateEntry(f"Group already has that user.")
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

    def get_all_group_ids(self) -> list[int]:
        """Method for getting list of all group ids"""
        ids_list_of_tuples = self.db.query(GroupUser.group_id.distinct()).all()
        ids = [x[0] for x in ids_list_of_tuples]
        return ids

    def get_all_group_members_ids(self, group_id: int) -> list[int]:
        """Method for getting members of group by id"""
        ids_list_of_tuples = self.db.query(GroupUser.user_id).filter(GroupUser.group_id == group_id).all()
        ids = [x[0] for x in ids_list_of_tuples]
        return ids

    def delete_group_user(self, group_id: int, user_id: int) -> bool:
        """Method for deleting group user"""
        group_user = self.db.query(GroupUser).filter \
            (and_(GroupUser.group_id == group_id, GroupUser.user_id == user_id)).first()
        if group_user is None:
            return False
        self.db.delete(group_user)
        self.db.commit()
        return True
