from fastapi import APIRouter

from app.groups.controller.groups_controller import GroupController
from app.groups.schema import GroupSchema, GroupSchemaIn


group_router = APIRouter(prefix="/api/users/groups", tags=["Groups"])


@group_router.get("/get-all", response_model=list[GroupSchema])
def get_all_groups():
    return GroupController.get_all()


@group_router.post("/add-group", response_model=GroupSchema)
def add_group(group: GroupSchemaIn):
    return GroupController.add_group(group_name=group.group_name, owner_user_name=group.owner_user_name,
                                     description=group.description)


@group_router.delete("/delete-group-by-id/{group_id}")
def delete_group_by_id(group_id: int):
    return GroupController.delete_group_by_id(group_id)

