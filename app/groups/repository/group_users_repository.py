"""Module for GroupUser repository"""
from typing import Type
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.groups.exceptions import DuplicateEntry, GroupNotFound, GroupUserNotFound
from app.groups.model import GroupUser, Group
from app.users.model import User


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

    def get_id_by_user_and_group_id(self, group_id: int, user_id: int) -> int:
        group_user_id_tuple = self.db.query(GroupUser.id).filter(and_(GroupUser.group_id == group_id,
                                                                      GroupUser.user_id == user_id)).first()
        if group_user_id_tuple is None:
            raise GroupUserNotFound(f"There is no data for group id {group_id} and user id {user_id}")
        return group_user_id_tuple[0]

    def get_user_name_by_group_user_id(self, group_user_id: int):
        group_user = self.db.query(GroupUser).filter(GroupUser.id == group_user_id).first()
        if group_user is None:
            raise GroupUserNotFound(f"There is no group user id {group_user_id}.")
        user = self.db.query(User.user_name).filter(User.id == group_user.user_id).first()
        return user[0]

    def get_group_id_by_group_user_id(self, group_user_id):
        group_id = self.db.query(GroupUser.group_id).filter(GroupUser.id == group_user_id).first()
        if group_id is None:
            raise GroupUserNotFound(f"No group user id {group_user_id}")
        return group_id[0]

    def check_if_user_is_part_of_group(self, group_name: str, user_id: int) -> bool:
        """Method for checking if user is part of group named in input."""
        if self.db.query(Group).filter(Group.group_name == group_name).first() is None:
            raise GroupUserNotFound(f"There is no group with name {group_name}")
        user = self.db.query(GroupUser).join(Group).filter(and_(Group.group_name == group_name,
                                                                GroupUser.user_id == user_id)).first()
        if user is None:
            return False
        return True

    def delete_group_user(self, group_id: int, user_id: int) -> bool:
        """Method for deleting group user"""
        group_user = self.db.query(GroupUser).filter \
            (and_(GroupUser.group_id == group_id, GroupUser.user_id == user_id)).first()
        if group_user is None:
            return False
        self.db.delete(group_user)
        self.db.commit()
        return True
