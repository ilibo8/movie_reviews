"""Module for Group controller"""
from fastapi import HTTPException
from fastapi.openapi.models import Response
from app.groups.exceptions import GroupNotFound, DuplicateEntry
from app.groups.service import GroupService


class GroupController:
    """Class for Group controller"""
    @staticmethod
    def add_group(group_name: str, group_owner_id: int, description: str):
        """Method for adding new group"""
        try:
            group = GroupService.add_group(group_name, group_owner_id, description)
            return group
        except DuplicateEntry as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def get_all():
        """Method for getting all groups"""
        try:
            groups = GroupService.get_all()
            return groups
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def delete_group_by_id(group_id: int):
        """Method for deleting group by id"""
        try:
            if GroupService.delete_by_id(group_id):
                return Response(content=f"Group with id {group_id} deleted .", status_code=200)
        except GroupNotFound as err:
            raise HTTPException(status_code=err.code, detail=err.message)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
