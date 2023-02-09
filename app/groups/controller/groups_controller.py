from fastapi import HTTPException
from fastapi.openapi.models import Response

from app.groups.exceptions import GroupNotFoundException
from app.groups.service import GroupService


class GroupController:

    @staticmethod
    def add_group(name: str, owner_user_name: str, description: str):
        try:
            return GroupService.add_group(name, owner_user_name, description)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_all():
        try:
            return GroupService.get_all()
        except GroupNotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def delete_group_by_id(group_id: int):
        try:
            if GroupService.delete_by_id(group_id):
                return Response(content=f"Group with id {group_id} deleted .", status_code=200)
        except GroupNotFoundException as e:
            raise HTTPException(status_code=e.code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
