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
        """
        The add_group_user function adds a user to a group.
        If there is no such group or if there is no such user, it raises an error.
        """
        try:
            with SessionLocal() as db:
                group_user_repository = GroupUserRepository(db)
                group_repository = GroupRepository(db)
                user_repository = UserRepository(db)
                group = group_repository.get_group_by_name(group_name)
                if group is None:
                    raise GroupNotFound(f"There is no group with name {group_name}")
                group_user_repository.add_group_user(group.id, user_id)
                members_ids = group_user_repository.get_all_group_members_ids(group.id)
                owner_user_name = user_repository.get_user_name_by_user_id(group.owner_id)
                members_names = [user_repository.get_user_name_by_user_id(id) for id in members_ids]
                members_names.sort()
                return {"group_name": group_name, "owner_user_name": owner_user_name,
                        "description": group.description, "date_created": group.date_created,
                        "group_users": members_names}
        except GroupNotFound as err:
            raise GroupNotFound(err.message) from err
        except DuplicateEntry as err:
            raise err
        except IntegrityError as err:
            raise err

    @staticmethod
    def get_all_joined() -> list[dict]:
        """
        The get_all_joined function returns a list of dictionaries, where each dictionary contains the following:
            - group_name: The name of the group.
            - owner_user_name: The name of the user who owns this group.
            - description: A description for this particular group.
            - date_created: When this particular group was created.

        """
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
    def get_all_groups_having_user_by_user_id(user_id: int) -> list[str]:
        """
        The function returns a list of all groups user is part of.
        """
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            group_repository = GroupRepository(db)
            group_ids = group_user_repository.get_all_groups_having_user_by_user_id(user_id)
            if len(group_ids) == 0:
                raise GroupNotFound("Not part of any group yet.")
            group_names = [group_repository.get_group_name_by_id(g_id) for g_id in group_ids]
            return group_names

    @staticmethod
    def delete_group_user(group_id: int, user_id: int):
        """
        The delete_group_user function deletes a user from a group.
        """
        with SessionLocal() as db:
            group_user_repository = GroupUserRepository(db)
            return group_user_repository.delete_group_user(group_id, user_id)
