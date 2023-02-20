"""Module for Group controller"""
from fastapi import HTTPException
from starlette.responses import Response
from app.groups.exceptions import GroupNotFound, DuplicateEntry, Unauthorized
from app.groups.service import GroupService


class GroupController:
    """Class for Group controller"""
    @staticmethod
    def add_group(group_name: str, group_owner_id: int, description: str):
        """
        The add_group function adds a new group to the database.
        """
        try:
            return GroupService.add_group(group_name, group_owner_id, description)
        except DuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err

    @staticmethod
    def get_all():
        """
        The get_all function returns all groups in the database.
        """
        try:
            groups = GroupService.get_all()
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
    def delete_group_by_name(group_name: str):
        """
        The delete_group_by_name function deletes a group by name.
        """
        try:
            if GroupService.delete_by_id(group_name):
                return Response(content=f"Group {group_name} deleted.", status_code=200)
        except GroupNotFound as err:
            raise HTTPException(status_code=400, detail=str(err)) from err
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err)) from err
