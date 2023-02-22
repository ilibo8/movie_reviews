"""Module for Group controller"""
from fastapi import HTTPException
from starlette.responses import Response
from app.groups.exceptions import GroupNotFound, DuplicateEntry, Unauthorized, GroupUserNotFound
from app.groups.service import GroupService
from app.users.exceptions import TokenExpired


class GroupController:
    """Class for Group controller"""
    @staticmethod
    def add_group(group_name: str, owner_user_id: int, description: str):
        """
        The add_group function adds a new group to the database.
        """
        try:
            return GroupService.add_group(group_name, owner_user_id, description)
        except TokenExpired as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except DuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all():
        """
        The function returns all groups in the database for superuser.
        """
        try:
            groups = GroupService.get_all()
            return groups
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_group_users():
        """
        The function returns a list of all groups and their users.
        """
        try:
            return GroupService.get_all_group_users()
        except GroupUserNotFound as err:
            raise HTTPException(status_code=404, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all_reformatted():
        """
        The returns all groups in the database.
        """
        try:
            groups = GroupService.get_all_reformatted()
            return groups
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def change_group_name(group_name: str, new_name: str, user_id: int):
        """
        The change_group_name function is used to change the name of a group.
        """
        try:
            return GroupService.change_group_name(group_name=group_name, new_name=new_name, user_id=user_id)
        except Unauthorized as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except GroupNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except DuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def delete_group_by_id(group_id: int):
        """
        The function deletes a group by id.
        """
        try:
            if GroupService.delete_by_id(group_id):
                return Response(content=f"Group with id {group_id} deleted.", status_code=200)
        except GroupNotFound as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

