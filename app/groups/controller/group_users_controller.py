"""Module for GroupUser controller"""
from fastapi import HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.exc import IntegrityError
from app.groups.exceptions import DuplicateEntry, GroupNotFound
from app.groups.service import GroupUserService


class GroupUserController:
    """Class for GroupUser controller"""
    @staticmethod
    def add_group_user(group_name: str, user_id: int):
        """
        The add_group_user function adds a user to a group.
        """
        try:
            group_user = GroupUserService.add_group_user(group_name, user_id)
            return group_user
        except GroupNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except DuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except IntegrityError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_joined():
        """
        The get_all_joined function returns a list of all the groups that the user is in.
        """
        try:
            return GroupUserService.get_all_joined()
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all_group_members(group_id: int):
        """
        The get_all_group_members function returns all the members of a group.
        """
        try:
            return GroupUserService.get_all_group_members(group_id)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_group_use(group_id: int, user_id: int):
        """
        The delete_group_use function is used to remove a user from a group.
        """
        try:
            if GroupUserService.delete_group_user(group_id, user_id):
                return Response(content=f"User with id {user_id} is removed from group {group_id}.", status_code=200)
            return Response(content=f"User with id {user_id} and group id {group_id} not found.", status_code=400)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
