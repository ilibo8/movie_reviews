"""Module for GroupUser repository"""
from typing import Type
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.groups.exceptions import DuplicateEntry, GroupUserNotFound
from app.groups.model import GroupUser, Group
from app.users.model import User


class GroupUserRepository:
    """Class for GroupUser repository"""

    def __init__(self, dbs: Session):
        self.dbs = dbs

    def add_group_user(self, group_id: int, user_id: int) -> GroupUser:
        """
        The add_group_user function adds a user to a group.
        """
        try:
            if self.dbs.query(GroupUser).filter(and_(GroupUser.group_id == group_id,
                                                     GroupUser.user_id == user_id)).first() is not None:
                raise DuplicateEntry("Group already has that user.")
            group_user = GroupUser(group_id, user_id)
            self.dbs.add(group_user)
            self.dbs.commit()
            self.dbs.refresh(group_user)
            return group_user
        except IntegrityError as err:
            raise err

    def get_all(self) -> list[Type[GroupUser]]:
        """
        The get_all function returns a list of all the group_users in the database.
        """
        group_user = self.dbs.query(GroupUser).all()
        return group_user

    def get_all_group_members_ids(self, group_id: int) -> list[int]:
        """
        The get_all_group_members_ids function accepts a group_id as an argument and returns a list of all the user ids
        that are members of that group.
        """
        ids_list_of_tuples = self.dbs.query(GroupUser.user_id).filter(GroupUser.group_id == group_id).all()
        ids = [x[0] for x in ids_list_of_tuples]
        return ids

    def get_id_by_user_and_group_id(self, group_id: int, user_id: int) -> int:
        """
        It queries the database for a GroupUser object with the given group_id and user_id.
        If no such object exists, it raises an exception. If it does exist, it returns the id of that object.
        """
        group_user_id_tuple = self.dbs.query(GroupUser.id).filter(and_(GroupUser.group_id == group_id,
                                                                       GroupUser.user_id == user_id)).first()
        if group_user_id_tuple is None:
            raise GroupUserNotFound(f"There is no data for group id {group_id} and user id {user_id}")
        return group_user_id_tuple[0]

    def get_user_name_by_group_user_id(self, group_user_id: int):
        """
        The get_user_name_by_group_user_id function takes a group user id and returns the corresponding user_name.
        If there is no group user with that id, it raises a GroupUserNotFound exception.
        """
        group_user = self.dbs.query(GroupUser).filter(GroupUser.id == group_user_id).first()
        if group_user is None:
            raise GroupUserNotFound(f"There is no group user id {group_user_id}.")
        user = self.dbs.query(User.user_name).filter(User.id == group_user.user_id).first()
        return user[0]

    def get_group_id_by_group_user_id(self, group_user_id):
        """
        The get_group_id_by_group_user_id function takes a group user id and returns the corresponding group id.
        It is used to get the group_id from GroupUser table by providing the group_user_id.
        """
        group_id = self.dbs.query(GroupUser.group_id).filter(GroupUser.id == group_user_id).first()
        if group_id is None:
            raise GroupUserNotFound(f"No group user id {group_user_id}")
        return group_id[0]

    def check_if_user_is_part_of_group(self, group_name: str, user_id: int) -> bool:
        """
        The check_if_user_is_part_of_group function checks if a user is part of a group.
        """
        if self.dbs.query(Group).filter(Group.group_name == group_name).first() is None:
            raise GroupUserNotFound(f"There is no group with name {group_name}")
        user = self.dbs.query(GroupUser).join(Group).filter(and_(Group.group_name == group_name,
                                                                 GroupUser.user_id == user_id)).first()
        if user is None:
            return False
        return True

    def delete_group_user(self, group_id: int, user_id: int) -> bool:
        """
        The delete_group_user function deletes a group user from the database.
        """
        group_user = self.dbs.query(GroupUser).filter \
            (and_(GroupUser.group_id == group_id, GroupUser.user_id == user_id)).first()
        if group_user is None:
            return False
        self.dbs.delete(group_user)
        self.dbs.commit()
        return True
